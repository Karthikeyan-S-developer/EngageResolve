import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Student } from '../services/types';
import { EngagementBadge } from './EngagementBadge';
import { COLORS, SPACING } from '../constants/theme';

interface StudentCardProps {
  student: Student;
  onPress: () => void;
}

export const StudentCard: React.FC<StudentCardProps> = ({ student, onPress }) => {
  const trendSymbol = student.trend === 'UP' ? '↑' : student.trend === 'DOWN' ? '↓' : '→';
  const trendColor = student.trend === 'UP' ? COLORS.high : student.trend === 'DOWN' ? COLORS.low : COLORS.textMuted;

  return (
    <TouchableOpacity style={styles.card} onPress={onPress} activeOpacity={0.7}>
      <View style={styles.left}>
        <Text style={styles.name}>{student.display_name}</Text>
        <Text style={styles.subtext}>ID: {student.id} • Version {student.state_version}</Text>
      </View>

      <View style={styles.right}>
        <EngagementBadge score={student.current_engagement} />
        
        <View style={styles.metaRow}>
          <Text style={[styles.trend, { color: trendColor }]}>{trendSymbol} {student.trend}</Text>
          {student.conflicts_count > 0 && (
            <Text style={styles.conflictCount}>{student.conflicts_count} Conflicts</Text>
          )}
        </View>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: COLORS.bgSurface,
    borderRadius: 8,
    padding: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.border,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  left: {
    flex: 1,
  },
  name: {
    fontSize: 15,
    fontWeight: '700',
    color: COLORS.textPrimary,
  },
  subtext: {
    fontSize: 12,
    color: COLORS.textMuted,
    marginTop: 2,
  },
  right: {
    alignItems: 'flex-end',
  },
  metaRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 4,
  },
  trend: {
    fontSize: 12,
    fontWeight: '700',
    marginRight: 8,
  },
  conflictCount: {
    fontSize: 11,
    fontWeight: '600',
    color: COLORS.conflict,
    backgroundColor: COLORS.conflictBg,
    paddingHorizontal: 6,
    paddingVertical: 1,
    borderRadius: 4,
  },
});
