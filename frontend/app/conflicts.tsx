import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, ActivityIndicator } from 'react-native';
import { ApiService } from '../services/api';
import { AuditLog } from '../services/types';
import { DecisionTrace } from '../components/DecisionTrace';
import { EmptyState } from '../components/EmptyState';
import { COLORS, SPACING } from '../constants/theme';

export default function ConflictsScreen() {
  const [loading, setLoading] = useState(true);
  const [conflicts, setConflicts] = useState<AuditLog[]>([]);
  const [error, setError] = useState<string | null>(null);

  const fetchConflicts = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await ApiService.getConflicts(150);
      setConflicts(data.conflicts || []);
    } catch (err: any) {
      setError(err.message || 'Failed to load conflict resolution records.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchConflicts();
  }, []);

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Multi-Camera Conflict Resolutions</Text>
        <Text style={styles.subtitle}>
          Detailed inspection of overlapping camera observations resolved via the 6-tier deterministic rule engine
        </Text>
      </View>

      {loading ? (
        <View style={styles.center}>
          <ActivityIndicator size="large" color={COLORS.primary} />
        </View>
      ) : error ? (
        <EmptyState title="Error Loading Conflicts" message={error} onRetry={fetchConflicts} />
      ) : (
        <FlatList
          data={conflicts}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => <DecisionTrace audit={item} />}
          contentContainerStyle={styles.listContent}
          ListEmptyComponent={
            <EmptyState title="No Camera Signal Conflicts" message="All camera observations were sequential and non-overlapping." />
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
