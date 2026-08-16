import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { AuditLog, DecisionLogic, CandidateEvent } from '../services/types';
import { ConflictIndicator } from './ConflictIndicator';
import { COLORS, SPACING } from '../constants/theme';

interface DecisionTraceProps {
  audit: AuditLog;
}

export const DecisionTrace: React.FC<DecisionTraceProps> = ({ audit }) => {
  const logic: DecisionLogic = (audit.resolution_logic as DecisionLogic) || {};
  const candidates: CandidateEvent[] = logic.candidate_events || [];

  return (
    <View style={styles.card}>
      <View style={styles.header}>
        <ConflictIndicator type={audit.decision_type} />
        <Text style={styles.timestamp}>{audit.timestamp}</Text>
      </View>

      <Text style={styles.explanationText}>
        {audit.human_readable_explanation || logic.reason || 'Decision recorded deterministically.'}
      </Text>

      {candidates.length > 0 && (
        <View style={styles.candidateContainer}>
          <Text style={styles.sectionHeader}>Competing Signals Evaluated:</Text>
          {candidates.map((c, idx) => (
            <View key={`cand-${idx}`} style={styles.candidateRow}>
              <Text style={styles.candCam}>• {c.camera_id || 'Camera Signal'}:</Text>
              <Text style={styles.candScore}>Score: {c.score.toFixed(2)}</Text>
              <Text style={styles.candConf}>Confidence: {(c.confidence * 100).toFixed(0)}%</Text>
            </View>
          ))}
        </View>
      )}

      {logic.tiebreaker_used && (
        <View style={styles.tiebreakBox}>
          <Text style={styles.tiebreakLabel}>
            Tie-Break Step Applied: <Text style={styles.tiebreakVal}>{logic.tiebreaker_used}</Text>
          </Text>
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
    padding: SPACING.md,
    marginBottom: SPACING.sm,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  timestamp: {
    fontSize: 12,
    color: COLORS.textMuted,
  },
  explanationText: {
    fontSize: 14,
    color: COLORS.textPrimary,
    lineHeight: 20,
    fontWeight: '500',
  },
  candidateContainer: {
    marginTop: SPACING.sm,
    backgroundColor: COLORS.bgSurfaceSecondary,
    borderRadius: 6,
    padding: SPACING.sm,
  },
  sectionHeader: {
    fontSize: 12,
    fontWeight: '700',
    color: COLORS.textSecondary,
    marginBottom: 4,
  },
  candidateRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginVertical: 2,
  },
  candCam: {
    fontSize: 12,
    fontWeight: '600',
    color: COLORS.textPrimary,
  },
  candScore: {
    fontSize: 12,
    color: COLORS.primary,
    fontWeight: '600',
  },
  candConf: {
    fontSize: 12,
    color: COLORS.textSecondary,
  },
  tiebreakBox: {
    marginTop: SPACING.sm,
    paddingTop: SPACING.xs,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
  },
  tiebreakLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
  },
  tiebreakVal: {
    fontWeight: '700',
    color: COLORS.conflict,
  },
});
