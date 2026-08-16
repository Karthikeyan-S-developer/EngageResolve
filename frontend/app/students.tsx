import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, TextInput, TouchableOpacity, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
import { ApiService } from '../services/api';
import { Student } from '../services/types';
import { StudentCard } from '../components/StudentCard';
import { EmptyState } from '../components/EmptyState';
import { COLORS, SPACING } from '../constants/theme';

export default function StudentsScreen() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [students, setStudents] = useState<Student[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<'ALL' | 'HIGH' | 'MODERATE' | 'LOW'>('ALL');
  const [error, setError] = useState<string | null>(null);

  const fetchStudents = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await ApiService.getStudents();
      setStudents(data);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch student roster.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  const filteredStudents = students.filter((s) => {
    const matchesSearch =
      s.display_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      s.id.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === 'ALL' || s.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <View style={styles.container}>
      <View style={styles.headerBox}>
        <Text style={styles.title}>Classroom Roster & Engagement Ranking</Text>
        <Text style={styles.subtitle}>Reconciled student states derived from multi-camera ingestion</Text>

        {/* Search Bar */}
        <TextInput
          style={styles.searchInput}
          placeholder="Search by student name or ID..."
          placeholderTextColor={COLORS.textMuted}
          value={searchQuery}
          onChangeText={setSearchQuery}
        />

        {/* Filter Pills */}
        <View style={styles.filterRow}>
          {(['ALL', 'HIGH', 'MODERATE', 'LOW'] as const).map((filter) => (
            <TouchableOpacity
              key={filter}
              style={[styles.filterPill, statusFilter === filter && styles.filterPillActive]}
              onPress={() => setStatusFilter(filter)}
            >
              <Text style={[styles.filterText, statusFilter === filter && styles.filterTextActive]}>
                {filter}
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
        <EmptyState title="Error Loading Roster" message={error} onRetry={fetchStudents} />
      ) : (
        <FlatList
          data={filteredStudents}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <StudentCard
              student={item}
              onPress={() => router.push(`/student/${item.id}` as any)}
            />
          )}
          contentContainerStyle={styles.listContent}
          ListEmptyComponent={
            <EmptyState
              title="No Matching Students Found"
              message="Try adjusting your search query or filter selection."
            />
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
  headerBox: {
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
  searchInput: {
    backgroundColor: COLORS.bgSurfaceSecondary,
    borderWidth: 1,
    borderColor: COLORS.border,
    borderRadius: 6,
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
    fontSize: 14,
    color: COLORS.textPrimary,
    marginBottom: SPACING.sm,
  },
  filterRow: {
    flexDirection: 'row',
  },
  filterPill: {
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.xs,
    borderRadius: 16,
    backgroundColor: COLORS.bgSurfaceSecondary,
    marginRight: SPACING.xs,
  },
  filterPillActive: {
    backgroundColor: COLORS.primary,
  },
  filterText: {
    fontSize: 12,
    fontWeight: '600',
    color: COLORS.textSecondary,
  },
  filterTextActive: {
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
