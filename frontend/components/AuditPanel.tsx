import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { AuditLog } from '../services/types';
import { DecisionTrace } from './DecisionTrace';
import { SPACING } from '../constants/theme';

interface AuditPanelProps {
  audits: AuditLog[];
}

export const AuditPanel: React.FC<AuditPanelProps> = ({ audits }) => {
  if (!audits || audits.length === 0) {
    return (
      <View style={styles.empty}>
        <Text style={styles.emptyText}>No audit traces recorded for this student.</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {audits.map((a) => (
        <DecisionTrace key={`audit-${a.id}`} audit={a} />
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingVertical: SPACING.sm,
  },
  empty: {
    padding: SPACING.lg,
    alignItems: 'center',
  },
  emptyText: {
    fontSize: 14,
    color: '#94A3B8',
  },
});
