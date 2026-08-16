import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS, SPACING } from '../constants/theme';

interface DashboardHeaderProps {
  title?: string;
  subtitle?: string;
}

export const DashboardHeader: React.FC<DashboardHeaderProps> = ({
  title = 'EngageResolve',
  subtitle = 'Classroom Engagement Intelligence Engine',
}) => {
  return (
    <View style={styles.headerContainer}>
      <View style={styles.left}>
        <View style={styles.logoBadge}>
          <Text style={styles.logoBadgeText}>ER</Text>
        </View>
        <View>
          <Text style={styles.title}>{title}</Text>
          <Text style={styles.subtitle}>{subtitle}</Text>
        </View>
      </View>

      <View style={styles.statusPill}>
        <View style={styles.liveDot} />
        <Text style={styles.statusText}>ENGINE ACTIVE</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  headerContainer: {
    backgroundColor: COLORS.bgHeader,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: COLORS.borderDark,
  },
  left: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  logoBadge: {
    width: 36,
    height: 36,
    borderRadius: 8,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.md,
  },
  logoBadgeText: {
    color: COLORS.textInverse,
    fontWeight: '800',
    fontSize: 16,
  },
  title: {
    fontSize: 18,
    fontWeight: '800',
    color: COLORS.textInverse,
    letterSpacing: 0.5,
  },
  subtitle: {
    fontSize: 12,
    color: COLORS.textMuted,
  },
  statusPill: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(5, 150, 105, 0.15)',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: COLORS.high,
  },
  liveDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: COLORS.high,
    marginRight: 6,
  },
  statusText: {
    fontSize: 10,
    fontWeight: '700',
    color: COLORS.high,
    letterSpacing: 0.5,
  },
});
