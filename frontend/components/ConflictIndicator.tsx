import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS } from '../constants/theme';

interface ConflictIndicatorProps {
  type: string;
}

export const ConflictIndicator: React.FC<ConflictIndicatorProps> = ({ type }) => {
  let label = type;
  let bg = COLORS.duplicateBg;
  let text = COLORS.duplicate;

  if (type === 'CONFLICT_RESOLUTION') {
    label = 'CONFLICT RESOLVED';
    bg = COLORS.conflictBg;
    text = COLORS.conflict;
  } else if (type === 'OUT_OF_ORDER_EVENT') {
    label = 'OUT-OF-ORDER REORDERED';
    bg = COLORS.outOfOrderBg;
    text = COLORS.outOfOrder;
  } else if (type === 'IDENTITY_RESOLUTION') {
    label = 'IDENTITY MATCHED';
    bg = COLORS.identityBg;
    text = COLORS.identity;
  } else if (type === 'DUPLICATE_EVENT') {
    label = 'DUPLICATE IGNORED';
    bg = COLORS.duplicateBg;
    text = COLORS.duplicate;
  }

  return (
    <View style={[styles.badge, { backgroundColor: bg }]}>
      <Text style={[styles.text, { color: text }]}>{label}</Text>
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
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 0.5,
  },
});
