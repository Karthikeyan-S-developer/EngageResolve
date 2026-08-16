import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS, THRESHOLDS } from '../constants/theme';

interface EngagementBadgeProps {
  score: number;
  showScore?: boolean;
}

export const EngagementBadge: React.FC<EngagementBadgeProps> = ({ score, showScore = true }) => {
  let label = 'MODERATE';
  let bgColor = COLORS.moderateBg;
  let textColor = COLORS.moderate;

  if (score >= THRESHOLDS.HIGH_ENGAGEMENT) {
    label = 'HIGH';
    bgColor = COLORS.highBg;
    textColor = COLORS.high;
  } else if (score < THRESHOLDS.LOW_ENGAGEMENT) {
    label = 'LOW';
    bgColor = COLORS.lowBg;
    textColor = COLORS.low;
  }

  return (
    <View style={[styles.badge, { backgroundColor: bgColor }]}>
      <Text style={[styles.text, { color: textColor }]}>
        {label} {showScore ? `(${(score * 100).toFixed(0)}%)` : ''}
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  badge: {
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 4,
    alignSelf: 'flex-start',
  },
  text: {
    fontSize: 11,
    fontWeight: '700',
    letterSpacing: 0.3,
  },
});
