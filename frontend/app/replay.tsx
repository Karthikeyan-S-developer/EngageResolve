import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { ApiService } from '../services/api';
import { ReplayResult } from '../services/types';
import { ReplayControls } from '../components/ReplayControls';
import { COLORS, SPACING } from '../constants/theme';

export default function ReplayScreen() {
  const [loading, setLoading] = useState(false);
  const [replayResult, setReplayResult] = useState<ReplayResult | null>(null);
  const [currentStep, setCurrentStep] = useState(0);

  const handleStartReplay = async () => {
    try {
      setLoading(true);
      const res = await ApiService.startReplay({});
      setReplayResult(res);
      setCurrentStep(0);
    } catch (err: any) {
      Alert.alert('Replay Error', err.message || 'Failed to execute replay run.');
    } finally {
      setLoading(false);
    }
  };

  const handleNextStep = () => {
    if (replayResult && currentStep < replayResult.event_count - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleReset = () => {
    setCurrentStep(0);
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.title}>Side-Effect-Free Replay Simulator</Text>
        <Text style={styles.subtitle}>
          Executes historical engagement events in an isolated in-memory sandbox engine to produce deterministic state result hashes.
        </Text>
      </View>

      <ReplayControls
        onStartReplay={handleStartReplay}
        isLoading={loading}
        replayResult={replayResult}
        currentStep={currentStep}
        totalSteps={replayResult?.event_count || 0}
        onNextStep={handleNextStep}
        onPrevStep={handlePrevStep}
        onReset={handleReset}
      />

      {replayResult && (
        <View style={styles.explanationBox}>
          <Text style={styles.boxTitle}>Replay Verification Guarantee</Text>
          <Text style={styles.boxText}>
            • Replay executed in isolated SQLite memory transaction without mutating production database tables.{'\n'}
            • Re-sorted all ingested events deterministically by timestamp, camera ID, and SHA-256 fingerprint.{'\n'}
            • Resulting state & audit history SHA-256 hash is <Text style={{ fontWeight: '700' }}>100% reproducible</Text> across multiple runs.
          </Text>
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.bgApp,
  },
  content: {
    padding: SPACING.md,
  },
  header: {
    marginBottom: SPACING.md,
  },
  title: {
    fontSize: 20,
    fontWeight: '800',
    color: COLORS.textPrimary,
  },
  subtitle: {
    fontSize: 13,
    color: COLORS.textMuted,
    marginTop: 4,
    lineHeight: 18,
  },
  explanationBox: {
    backgroundColor: COLORS.highBg,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: COLORS.high,
    padding: SPACING.md,
    marginTop: SPACING.sm,
  },
  boxTitle: {
    fontSize: 14,
    fontWeight: '700',
    color: COLORS.high,
    marginBottom: 4,
  },
  boxText: {
    fontSize: 13,
    color: COLORS.textPrimary,
    lineHeight: 20,
  },
});
