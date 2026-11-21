<?php

/**
 * Preview or remove only session-owned demo entities from an exact manifest.
 *
 * Copy into the reviewed project mount, then run through Drush with environment:
 * SEC_REVIEW_MANIFEST=/var/www/html/demo-cleanup.json (required)
 * SEC_REVIEW_APPLY=1 (only after reviewing the preview; default never deletes)
 *
 * Manifest example using synthetic IDs and exact current labels/usernames:
 * {"node":[{"id":42,"label":"owned demo"}],
 *  "user":[{"id":17,"label":"secdemo_editor"}]}
 * Supported types: node, block_content, user. Other demo setup needs separate
 * reviewed cleanup. Do not build the manifest by searching common title markers.
 */

$manifestPath = getenv('SEC_REVIEW_MANIFEST');
if (!$manifestPath || !is_file($manifestPath)) {
  throw new \RuntimeException('Set SEC_REVIEW_MANIFEST to an existing reviewed JSON file. No entities were deleted.');
}
$manifest = json_decode(file_get_contents($manifestPath), TRUE, 512, JSON_THROW_ON_ERROR);
if (!is_array($manifest) || !$manifest) {
  throw new \RuntimeException('Cleanup manifest must be a nonempty object of entity types and exact IDs/labels.');
}
$apply = getenv('SEC_REVIEW_APPLY') === '1';
$etm = \Drupal::entityTypeManager();
$pending = [];
$report = ['apply' => $apply, 'entities' => []];

// Resolve and verify the whole scope before deleting anything. No broad queries.
foreach ($manifest as $type => $rows) {
  if (!in_array($type, ['node', 'block_content', 'user'], TRUE) || !is_array($rows) || !$etm->hasDefinition($type)) {
    throw new \RuntimeException('Unsupported entity type or malformed rows in cleanup manifest.');
  }
  $storage = $etm->getStorage($type);
  foreach ($rows as $row) {
    if (!is_array($row) || !isset($row['id'], $row['label']) || !is_int($row['id']) || $row['id'] < 1 || !is_string($row['label']) || $row['label'] === '') {
      throw new \RuntimeException('Every cleanup row must specify a positive integer ID and exact nonempty label.');
    }
    if ($type === 'user' && ($row['id'] <= 1 || strpos($row['label'], 'secdemo_') !== 0)) {
      throw new \RuntimeException('Refusing cleanup of a protected or non-demo user.');
    }
    $entity = $storage->load($row['id']);
    if (!$entity) {
      $report['entities'][] = ['type' => $type, 'id' => $row['id'], 'status' => 'already absent'];
      continue;
    }
    if ((string) $entity->label() !== $row['label']) {
      throw new \RuntimeException("Identity mismatch for {$type} {$row['id']}; no entities were deleted.");
    }
    $pending[$type . ':' . $row['id']] = $entity;
    $report['entities'][] = ['type' => $type, 'id' => $row['id'], 'label' => $row['label'], 'status' => $apply ? 'delete requested' : 'would delete'];
  }
}
if ($apply) {
  foreach ($pending as $entity) {
    $entity->delete();
  }
}
print json_encode($report, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . "\n";
