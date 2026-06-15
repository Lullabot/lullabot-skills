<?php

/**
 * Security-review recon for a Drupal/DDEV site.
 *
 * Prints a JSON snapshot of the facts that decide whether a finding is real and
 * who can demonstrate it: roles + is_admin, per-role create access for nodes /
 * blocks / taxonomy terms, required & required-on-publish fields, reference-
 * field widgets, save-blocking default references, Layout Builder access, and
 * login-related modules.
 *
 * Run: copy to project root, then `ddev drush php:script .sec_recon.php`.
 * Read-only: creates only UNSAVED probe entities for access checks.
 */

use Drupal\Core\Session\AnonymousUserSession;
use Drupal\node\Entity\Node;
use Drupal\user\Entity\User;

$etm = \Drupal::entityTypeManager();
$out = [];

/**
 * Build an AccountInterface to test a role's access (no DB writes).
 *
 * Each probe gets a DISTINCT synthetic uid: entity access handlers cache
 * createAccess() by account id, so unsaved users sharing a null id would poison
 * each other's results (every role inherits the first one checked).
 */
$probeUid = 99000000;
$accountFor = function (string $rid) use (&$probeUid) {
  if ($rid === 'anonymous') {
    return new AnonymousUserSession();
  }
  $roles = $rid === 'authenticated' ? ['authenticated'] : ['authenticated', $rid];
  return User::create(['uid' => ++$probeUid, 'name' => '_probe_' . $rid, 'status' => 1, 'roles' => $roles]);
};

/** Reset an access handler's static cache before a fresh per-account check. */
$freshAccess = function ($handler, callable $check) {
  $handler->resetCache();
  return (bool) $check();
};

$safe = function (callable $fn, $fallback = null) {
  try { return $fn(); } catch (\Throwable $e) { return ['__error' => $e->getMessage()]; }
};

// --- Environment --------------------------------------------------------------
$out['environment'] = $safe(function () {
  return [
    'drupal_root' => DRUPAL_ROOT,
    'db_driver' => \Drupal::database()->driver(),
    'site_name' => \Drupal::config('system.site')->get('name'),
  ];
});

// --- Roles --------------------------------------------------------------------
$roleIds = [];
$out['roles'] = $safe(function () use ($etm, &$roleIds) {
  $rows = [];
  foreach ($etm->getStorage('user_role')->loadMultiple() as $role) {
    $roleIds[] = $role->id();
    $rows[] = [
      'id' => $role->id(),
      'label' => $role->label(),
      'is_admin' => (bool) $role->isAdmin(),
    ];
  }
  return $rows;
});

// --- Login-related modules + form protection ---------------------------------
$out['login'] = $safe(function () {
  $mh = \Drupal::moduleHandler();
  $watch = ['openid_connect','samlauth','cas','antibot','honeypot','captcha','tfa','password_policy'];
  $enabled = array_values(array_filter($watch, fn($m) => $mh->moduleExists($m)));
  $info = ['enabled_modules' => $enabled];
  if ($mh->moduleExists('honeypot')) {
    $h = \Drupal::config('honeypot.settings');
    $forms = $h->get('form_settings') ?: [];
    $info['honeypot'] = [
      'protect_all_forms' => (bool) $h->get('protect_all_forms'),
      'time_limit' => $h->get('time_limit'),
      'unprotected_forms' => $h->get('unprotected_forms'),
      'protected_forms' => array_keys(array_filter($forms)),
    ];
  }
  if ($mh->moduleExists('antibot')) {
    $info['antibot'] = ['form_ids' => \Drupal::config('antibot.settings')->get('form_ids')];
  }
  $info['note'] = $enabled
    ? 'SSO/bot-protection present — establish demo sessions with `drush uli --name=<user>` rather than the login form.'
    : 'Standard login form should be scriptable.';
  return $info;
});

// --- Text formats per role ----------------------------------------------------
$out['text_formats_by_role'] = $safe(function () use ($roleIds, $etm) {
  $map = [];
  foreach ($etm->getStorage('filter_format')->loadMultiple() as $fmt) {
    $perm = $fmt->getPermissionName();
    foreach ($roleIds as $rid) {
      $role = $etm->getStorage('user_role')->load($rid);
      if ($role && ($role->isAdmin() || ($perm && $role->hasPermission($perm)))) {
        $map[$rid][] = $fmt->id();
      }
    }
  }
  return $map;
});

// --- Node types: fields, publish requirements, widgets, create access --------
$out['node_types'] = $safe(function () use ($etm, $roleIds, $accountFor, $freshAccess) {
  $efm = \Drupal::service('entity_field.manager');
  $efdm = \Drupal::service('entity_display.repository');
  $ah = $etm->getAccessControlHandler('node');
  $rows = [];
  foreach ($etm->getStorage('node_type')->loadMultiple() as $type) {
    $bundle = $type->id();
    $entry = ['bundle' => $bundle];
    try {
      // Authoritative published-by-default for the bundle.
      $entry['published_default'] = (bool) ($type->get('status') ?? TRUE);
      $defs = $efm->getFieldDefinitions('node', $bundle);
      // Required (always) fields:
      $req = [];
      $refWidgets = [];
      $form = $efdm->getFormDisplay('node', $bundle, 'default');
      foreach ($defs as $name => $def) {
        if ($def->isRequired()) {
          $req[] = $name;
        }
        $comp = $form ? $form->getComponent($name) : null;
        if ($comp && in_array($def->getType(), ['entity_reference','entity_reference_revisions'], true)) {
          $refWidgets[$name] = $comp['type'] ?? 'unknown';
        }
      }
      $entry['required_fields'] = $req;
      $entry['reference_widgets'] = $refWidgets;
    } catch (\Throwable $e) {
      $entry['fields_error'] = $e->getMessage();
    }
    // Required-on-publish + blocking default refs: validate a published stub.
    try {
      $stub = Node::create(['type' => $bundle, 'status' => 1, 'title' => 'Recon Probe']);
      $violations = $stub->validate();
      $pub = [];
      foreach ($violations as $v) {
        $pub[] = ['field' => (string) $v->getPropertyPath(), 'message' => strip_tags((string) $v->getMessage())];
      }
      $entry['publish_violations'] = $pub;
    } catch (\Throwable $e) {
      $entry['publish_violations_error'] = $e->getMessage();
    }
    // Per-role create access.
    $acc = [];
    foreach ($roleIds as $rid) {
      $acc[$rid] = $freshAccess($ah, fn() => $ah->createAccess($bundle, $accountFor($rid)));
    }
    $entry['create_access'] = $acc;
    $rows[] = $entry;
  }
  return $rows;
});

// --- Block content bundles: per-role create access ---------------------------
$out['block_bundles'] = $safe(function () use ($etm, $roleIds, $accountFor, $freshAccess) {
  if (!$etm->hasDefinition('block_content')) {
    return ['__note' => 'block_content not present'];
  }
  $ah = $etm->getAccessControlHandler('block_content');
  $rows = [];
  foreach ($etm->getStorage('block_content_type')->loadMultiple() as $type) {
    $acc = [];
    foreach ($roleIds as $rid) {
      $acc[$rid] = $freshAccess($ah, fn() => $ah->createAccess($type->id(), $accountFor($rid)));
    }
    $rows[$type->id()] = ['create_access' => $acc];
  }
  return $rows;
});

// --- Taxonomy vocabularies: per-role create access ---------------------------
$out['vocabularies'] = $safe(function () use ($etm, $roleIds, $accountFor, $freshAccess) {
  if (!$etm->hasDefinition('taxonomy_vocabulary')) {
    return ['__note' => 'taxonomy not present'];
  }
  $ah = $etm->getAccessControlHandler('taxonomy_term');
  $rows = [];
  foreach ($etm->getStorage('taxonomy_vocabulary')->loadMultiple() as $vocab) {
    $acc = [];
    foreach ($roleIds as $rid) {
      // createAccess for terms keys on the vocabulary bundle.
      $acc[$rid] = $freshAccess($ah, fn() => $ah->createAccess($vocab->id(), $accountFor($rid)));
    }
    $rows[$vocab->id()] = ['create_access' => $acc];
  }
  return $rows;
});

// --- Layout Builder: enabled bundles + per-role override access --------------
$out['layout_builder'] = $safe(function () use ($etm, $roleIds, $accountFor) {
  $efdm = \Drupal::service('entity_display.repository');
  $am = \Drupal::service('access_manager');
  $enabled = [];
  foreach ($etm->getStorage('node_type')->loadMultiple() as $type) {
    $disp = $efdm->getViewDisplay('node', $type->id(), 'default');
    if ($disp && $disp->getThirdPartySetting('layout_builder', 'enabled')) {
      $enabled[$type->id()] = (bool) $disp->getThirdPartySetting('layout_builder', 'allow_custom');
    }
  }
  $access = [];
  foreach (array_keys($enabled) as $bundle) {
    $ids = \Drupal::entityQuery('node')->accessCheck(FALSE)->condition('type', $bundle)->range(0, 1)->execute();
    $nid = $ids ? reset($ids) : null;
    if (!$nid) { $access[$bundle] = '__no node to test__'; continue; }
    foreach ($roleIds as $rid) {
      try {
        $access[$bundle][$rid] = (bool) $am->checkNamedRoute('layout_builder.overrides.node.view', ['node' => $nid], $accountFor($rid));
      } catch (\Throwable $e) {
        $access[$bundle][$rid] = '__err__';
      }
    }
  }
  return ['enabled_bundles' => $enabled, 'override_view_access' => $access];
});

print json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . "\n";
