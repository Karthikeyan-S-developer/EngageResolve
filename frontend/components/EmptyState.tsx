import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { COLORS, SPACING } from '../constants/theme';

interface EmptyStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title = 'No Data Available',
  message = 'There are no records to display. Ensure the backend server is running and demo data is seeded.',
  onRetry,
}) => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>{title}</Text>
      <Text style={styles.message}>{message}</Text>
      {onRetry && (
        <TouchableOpacity style={styles.btn} onPress={onRetry}>
          <Text style={styles.btnText}>Retry Request</Text>
        </TouchableOpacity>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: SPACING.xl,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: COLORS.bgSurface,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: COLORS.border,
    marginVertical: SPACING.md,
  },
  title: {
    fontSize: 16,
    fontWeight: '700',
    color: COLORS.textPrimary,
    marginBottom: SPACING.xs,
  },
  message: {
    fontSize: 13,
    color: COLORS.textMuted,
    textAlign: 'center',
    marginBottom: SPACING.md,
    lineHeight: 18,
  },
  btn: {
    backgroundColor: COLORS.primary,
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
    borderRadius: 6,
  },
  btnText: {
    color: COLORS.textInverse,
    fontWeight: '600',
    fontSize: 13,
  },
});
