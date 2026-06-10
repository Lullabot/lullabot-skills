<?php

/**
 * Tear down everything the security-review skill planted.
 *
 * Deletes nodes/blocks whose title/label contains the demo marker, and the
 * throwaway test users (name prefix `secdemo_`). Adjust $MARKER / $USER_PREFIX
 * if you used different ones.
 *
 * Run: copy to project root, then `ddev drush php:script .sec_cleanup.php`.
 */

use Drupal\node\Entity\Node;
use Drupal\block_content\Entity\BlockContent;
use Drupal\user\Entity\User;

$MARKER = 'XSS FINDING';        // appears in every demo payload
$EXTRA_TITLES = ['SecReview PoC%']; // seeded vehicle content (LIKE patterns)
$USER_PREFIX = 'secdemo_';

$etm = \Drupal::entityTypeManager();
$report = [];

// Nodes: marker in title + any seeded vehicle titles.
$nids = \Drupal::entityQuery('node')->accessCheck(FALSE)
  ->condition('title', '%' . $MARKER . '%', 'LIKE')->execute();
foreach ($EXTRA_TITLES as $pat) {
  $nids += \Drupal::entityQuery('node')->accessCheck(FALSE)
    ->condition('title', $pat, 'LIKE')->execute();
}
foreach (Node::loadMultiple($nids) as $n) { $n->delete(); }
$report['nodes_deleted'] = count($nids);

// Content blocks: marker in info label.
if ($etm->hasDefinition('block_content')) {
  $bids = \Drupal::entityQuery('block_content')->accessCheck(FALSE)
    ->condition('info', '%' . $MARKER . '%', 'LIKE')->execute();
  foreach (BlockContent::loadMultiple($bids) as $b) { $b->delete(); }
  $report['blocks_deleted'] = count($bids);
}

// Throwaway test users.
$uids = \Drupal::entityQuery('user')->accessCheck(FALSE)
  ->condition('name', $USER_PREFIX . '%', 'LIKE')->execute();
foreach (User::loadMultiple($uids) as $u) {
  if ((int) $u->id() > 1) { $u->delete(); }
}
$report['users_deleted'] = count($uids);

print json_encode($report) . "\n";
