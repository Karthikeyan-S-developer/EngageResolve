import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { CameraStatus as CameraStatusType } from '../services/types';
import { COLORS, SPACING } from '../constants/theme';

interface CameraStatusProps {
  camera: CameraStatusType;
}

export const CameraStatus: React.FC<CameraStatusProps> = ({ camera }) => {
  const relPct = (camera.reliability * 100).toFixed(0);

  return (
    <View style={styles.card}>
      <View style={styles.header}>
        <View style={styles.statusDot} />
        <Text style={styles.camId}>{camera.camera_id}</Text>
      </View>
      
      <View style={styles.row}>
        <Text style={styles.label}>Reliability:</Text>
        <Text style={styles.val}>{relPct}%</Text>
      </View>
      <View style={styles.row}>
        <Text style={styles.label}>Events:</Text>
        <Text style={styles.val}>{camera.total_events}</Text>
      </View>
      <View style={styles.row}>
        <Text style={styles.label}>Avg Engagement:</Text>
        <Text style={styles.val}>{(camera.avg_engagement * 100).toFixed(0)}%</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: COLORS.bgSurface,
    borderRadius: 8,
    padding: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.border,
    minWidth: 150,
    margin: SPACING.xs,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: COLORS.high,
    marginRight: 6,
  },
  camId: {
    fontSize: 14,
    fontWeight: '700',
    color: COLORS.textPrimary,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 4,
  },
  label: {
    fontSize: 12,
    color: COLORS.textMuted,
  },
  val: {
    fontSize: 12,
    fontWeight: '600',
    color: COLORS.textSecondary,
  },
});
