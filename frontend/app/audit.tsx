import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, ActivityIndicator } from 'react-native';
import { ApiService } from '../services/api';
import { AuditLog } from '../services/types';
import { DecisionTrace } from '../components/DecisionTrace';
import { EmptyState } from '../components/EmptyState';
import { COLORS, SPACING } from '../constants/theme';

export default function AuditScreen() {
  const [loading, setLoading] = useState(true);
  const [audits, setAudits] = useState<AuditLog[]>([]);
  const [filterType, setFilterType] = useState<string>('ALL');
  const [error, setError] = useState<string | null>(null);

  const fetchAudits = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await ApiService.getAllAudits(300);
      setAudits(data.audit_logs || []);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch system audit logs.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAudits();
  }, []);

  const filteredAudits = audits.filter((a) => {
    if (filterType === 'ALL') return true;
    return a.decision_type === filterType;
  });

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>System Audit Trail & Decision Explanations</Text>
        <Text style={styles.subtitle}>
          Immutable log of all reconciliation, out-of-order reordering, and identity resolution decisions
        </Text>

        {/* Filter Pills */}
        <View style={styles.filterRow}>
          {[
            { label: 'All Audits', value: 'ALL' },
            { label: 'Conflicts', value: 'CONFLICT_RESOLUTION' },
            { label: 'Out-of-Order', value: 'OUT_OF_ORDER_EVENT' },
            { label: 'Identity Matches', value: 'IDENTITY_RESOLUTION' },
          ].map((f) => (
            <TouchableOpacity
              key={f.value}
              style={[styles.pill, filterType === f.value && styles.pillActive]}
              onPress={() => setFilterType(f.value)}
            >
              <Text style={[styles.pillText, filterType === f.value && styles.pillTextActive]}>
                {f.label}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      {loading ? (
        <View style={styles.center}>
          <ActivityIndicator size="large" color={COLORS.primary} />
        </View>
      ) : error ? (
        <EmptyState title="Error Loading Audit Trail" message={error} onRetry={fetchAudits} />
      ) : (
        <FlatList
          data={filteredAudits}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => <DecisionTrace audit={item} />}
          contentContainerStyle={styles.listContent}
          ListEmptyComponent={
            <EmptyState title="No Audit Records" message="No decisions match the selected filter." />
          }
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.bgApp,
  },
  header: {
    backgroundColor: COLORS.bgSurface,
    padding: SPACING.md,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  title: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.textPrimary,
  },
  subtitle: {
    fontSize: 12,
    color: COLORS.textMuted,
    marginTop: 2,
    marginBottom: SPACING.sm,
  },
  filterRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  pill: {
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.xs,
    borderRadius: 16,
    backgroundColor: COLORS.bgSurfaceSecondary,
    marginRight: SPACING.xs,
    marginBottom: SPACING.xs,
  },
  pillActive: {
    backgroundColor: COLORS.primary,
  },
  pillText: {
    fontSize: 12,
    fontWeight: '600',
    color: COLORS.textSecondary,
  },
  pillTextActive: {
    color: COLORS.textInverse,
  },
  listContent: {
    padding: SPACING.md,
  },
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
