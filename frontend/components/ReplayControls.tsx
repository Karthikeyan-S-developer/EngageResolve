import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ActivityIndicator } from 'react-native';
import { COLORS, SPACING } from '../constants/theme';
import { ReplayResult } from '../services/types';

interface ReplayControlsProps {
  onStartReplay: () => void;
  isLoading: boolean;
  replayResult: ReplayResult | null;
  currentStep: number;
  totalSteps: number;
  onNextStep: () => void;
  onPrevStep: () => void;
  onReset: () => void;
}

export const ReplayControls: React.FC<ReplayControlsProps> = ({
  onStartReplay,
  isLoading,
  replayResult,
  currentStep,
  totalSteps,
  onNextStep,
  onPrevStep,
  onReset,
}) => {
  return (
    <View style={styles.card}>
      <Text style={styles.title}>Deterministic Replay Simulator</Text>
      <Text style={styles.subtitle}>
        Re-evaluates raw historical events in a side-effect-free isolated engine sandbox.
      </Text>

      <TouchableOpacity
        style={[styles.btnPrimary, isLoading && styles.btnDisabled]}
        onPress={onStartReplay}
        disabled={isLoading}
      >
        {isLoading ? (
          <ActivityIndicator color={COLORS.textInverse} size="small" />
        ) : (
          <Text style={styles.btnPrimaryText}>▶ Start Side-Effect-Free Replay Run</Text>
        )}
      </TouchableOpacity>

      {replayResult && (
        <View style={styles.resultBox}>
          <View style={styles.row}>
            <Text style={styles.label}>Replay Status:</Text>
            <Text style={styles.statusCompleted}>{replayResult.status.toUpperCase()}</Text>
          </View>
          <View style={styles.row}>
            <Text style={styles.label}>Events Processed:</Text>
            <Text style={styles.val}>{replayResult.event_count}</Text>
          </View>
          <View style={styles.hashBox}>
            <Text style={styles.hashLabel}>Deterministic Result SHA-256 Hash:</Text>
            <Text style={styles.hashVal} numberOfLines={1}>
              {replayResult.result_hash}
            </Text>
          </View>

          {/* Stepper Controls */}
          {totalSteps > 0 && (
            <View style={styles.stepperContainer}>
              <Text style={styles.stepText}>
                Step {currentStep + 1} of {totalSteps}
              </Text>
              
              <View style={styles.stepperRow}>
                <TouchableOpacity
                  style={[styles.stepBtn, currentStep === 0 && styles.btnDisabled]}
                  onPress={onPrevStep}
                  disabled={currentStep === 0}
                >
                  <Text style={styles.stepBtnText}>◀ Previous Event</Text>
                </TouchableOpacity>

                <TouchableOpacity
                  style={[styles.stepBtn, currentStep >= totalSteps - 1 && styles.btnDisabled]}
                  onPress={onNextStep}
                  disabled={currentStep >= totalSteps - 1}
                >
                  <Text style={styles.stepBtnText}>Next Event ▶</Text>
                </TouchableOpacity>

                <TouchableOpacity style={styles.resetBtn} onPress={onReset}>
                  <Text style={styles.resetBtnText}>↺ Reset</Text>
                </TouchableOpacity>
              </View>
            </View>
          )}
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: COLORS.bgSurface,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: COLORS.border,
    padding: SPACING.lg,
    marginBottom: SPACING.md,
  },
  title: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.textPrimary,
  },
  subtitle: {
    fontSize: 13,
    color: COLORS.textMuted,
    marginTop: 4,
    marginBottom: SPACING.md,
  },
  btnPrimary: {
    backgroundColor: COLORS.primary,
    paddingVertical: SPACING.md,
    borderRadius: 6,
    alignItems: 'center',
  },
  btnDisabled: {
    opacity: 0.6,
  },
  btnPrimaryText: {
    color: COLORS.textInverse,
    fontSize: 14,
    fontWeight: '700',
  },
  resultBox: {
    marginTop: SPACING.md,
    backgroundColor: COLORS.bgSurfaceSecondary,
    borderRadius: 6,
    padding: SPACING.md,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginVertical: 4,
  },
  label: {
    fontSize: 13,
    color: COLORS.textSecondary,
  },
  statusCompleted: {
    fontSize: 12,
    fontWeight: '700',
    color: COLORS.high,
    backgroundColor: COLORS.highBg,
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
  },
  val: {
    fontSize: 13,
    fontWeight: '700',
    color: COLORS.textPrimary,
  },
  hashBox: {
    marginTop: SPACING.sm,
    paddingTop: SPACING.sm,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
  },
  hashLabel: {
    fontSize: 11,
    color: COLORS.textMuted,
    fontWeight: '600',
    textTransform: 'uppercase',
  },
  hashVal: {
    fontSize: 12,
    fontFamily: 'monospace',
    fontWeight: '700',
    color: COLORS.primary,
    marginTop: 2,
  },
  stepperContainer: {
    marginTop: SPACING.md,
    paddingTop: SPACING.md,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
  },
  stepText: {
    fontSize: 13,
    fontWeight: '700',
    color: COLORS.textPrimary,
    textAlign: 'center',
    marginBottom: SPACING.sm,
  },
  stepperRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  stepBtn: {
    backgroundColor: COLORS.bgSurface,
    borderWidth: 1,
    borderColor: COLORS.border,
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.md,
    borderRadius: 6,
  },
  stepBtnText: {
    fontSize: 12,
    fontWeight: '600',
    color: COLORS.textPrimary,
  },
  resetBtn: {
    backgroundColor: COLORS.lowBg,
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.md,
    borderRadius: 6,
  },
  resetBtnText: {
    fontSize: 12,
    fontWeight: '700',
    color: COLORS.low,
  },
});
