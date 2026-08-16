import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { TimelineItem } from '../services/types';
import { EngagementBadge } from './EngagementBadge';
import { ConflictIndicator } from './ConflictIndicator';
import { COLORS, SPACING } from '../constants/theme';

interface EventTimelineProps {
  timeline: TimelineItem[];
  selectedVersion?: number;
  onSelectVersion?: (item: TimelineItem) => void;
}

export const EventTimeline: React.FC<EventTimelineProps> = ({
  timeline,
  selectedVersion,
  onSelectVersion,
}) => {
  return (
    <View style={styles.container}>
      {timeline.map((item) => {
        const isSelected = selectedVersion === item.version;
        const timeStr = item.effective_timestamp.includes('T')
          ? item.effective_timestamp.split('T')[1].replace('Z', '')
          : item.effective_timestamp;

        return (
          <View
            key={`timeline-v${item.version}`}
            style={[styles.itemCard, isSelected && styles.selectedCard]}
          >
            <View style={styles.leftLine}>
              <View style={styles.dot} />
              <View style={styles.line} />
            </View>

            <View style={styles.content}>
              <View style={styles.headerRow}>
                <Text style={styles.timeStr}>{timeStr}</Text>
                <Text style={styles.versionTag}>Version {item.version}</Text>
              </View>

              <View style={styles.detailRow}>
                <View>
                  <Text style={styles.cameraText}>CAM: {item.camera_id} ({item.source})</Text>
                  <Text style={styles.confText}>Confidence: {(item.confidence * 100).toFixed(0)}%</Text>
                </View>

                <View style={styles.badgeCol}>
                  <EngagementBadge score={item.engagement_score} />
                  <View style={{ marginTop: 4 }}>
                    <ConflictIndicator type={item.state_status} />
                  </View>
                </View>
              </View>
            </View>
          </View>
        );
      })}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingVertical: SPACING.sm,
  },
  itemCard: {
    flexDirection: 'row',
    backgroundColor: COLORS.bgSurface,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: COLORS.border,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
  },
  selectedCard: {
    borderColor: COLORS.primary,
    backgroundColor: COLORS.primaryLight,
  },
  leftLine: {
    alignItems: 'center',
    marginRight: SPACING.md,
  },
  dot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: COLORS.primary,
    marginTop: 4,
  },
  line: {
    width: 2,
    flex: 1,
    backgroundColor: COLORS.border,
    marginTop: 4,
  },
  content: {
    flex: 1,
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  timeStr: {
    fontSize: 14,
    fontWeight: '700',
    color: COLORS.textPrimary,
  },
  versionTag: {
    fontSize: 11,
    fontWeight: '600',
    color: COLORS.textMuted,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 4,
  },
  cameraText: {
    fontSize: 13,
    fontWeight: '600',
    color: COLORS.textSecondary,
  },
  confText: {
    fontSize: 12,
    color: COLORS.textMuted,
    marginTop: 2,
  },
  badgeCol: {
    alignItems: 'flex-end',
  },
});
