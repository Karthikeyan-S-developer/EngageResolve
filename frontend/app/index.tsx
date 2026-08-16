import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl, ActivityIndicator, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { ApiService } from '../services/api';
import { DashboardSummary, CameraStatus as CameraStatusType, Student, AuditLog } from '../services/types';
import { StatCard } from '../components/StatCard';
import { CameraStatus } from '../components/CameraStatus';
import { StudentCard } from '../components/StudentCard';
import { DecisionTrace } from '../components/DecisionTrace';
import { EmptyState } from '../components/EmptyState';
import { COLORS, SPACING } from '../constants/theme';

export default function DashboardScreen() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [cameras, setCameras] = useState<CameraStatusType[]>([]);
  const [students, setStudents] = useState<Student[]>([]);
  const [recentConflicts, setRecentConflicts] = useState<AuditLog[]>([]);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    try {
      setError(null);
      const [sumRes, camRes, stuRes, confRes] = await Promise.all([
        ApiService.getDashboardSummary(),
        ApiService.getCameraSummaries(),
        ApiService.getStudents(),
        ApiService.getConflicts(3),
      ]);
      setSummary(sumRes);
      setCameras(camRes);
      setStudents(stuRes);
      setRecentConflicts(confRes.conflicts || []);
    } catch (err: any) {
      setError(err.message || 'Failed to load dashboard metrics.');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    loadData();
  };

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color={COLORS.primary} />
        <Text style={styles.loadingText}>Fetching real-time classroom analytics...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.paddingContainer}>
        <EmptyState title="Backend Connection Failed" message={error} onRetry={loadData} />
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.contentContainer}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
    >
      <View style={styles.sectionHeader}>
        <Text style={styles.sectionTitle}>Real-Time Classroom Metrics</Text>
        <Text style={styles.sectionSubtitle}>Live observations & reconciled state timeline engine</Text>
      </View>

      {/* KPI Cards Grid */}
      <View style={styles.grid}>
        <StatCard
          title="Total Students"
          value={summary?.total_students || 0}
          subtitle="Monitored in classroom"
          badge="ACTIVE"
          badgeColor={COLORS.high}
          badgeBg={COLORS.highBg}
        />
        <StatCard
          title="Events Ingested"
          value={summary?.total_events || 0}
          subtitle="Multi-camera signals"
        />
        <StatCard
          title="Avg Engagement"
          value={`${((summary?.average_engagement || 0) * 100).toFixed(1)}%`}
          subtitle="Reconciled timeline"
          badge={summary?.average_engagement! >= 0.75 ? 'HIGH' : 'MODERATE'}
          badgeColor={summary?.average_engagement! >= 0.75 ? COLORS.high : COLORS.moderate}
          badgeBg={summary?.average_engagement! >= 0.75 ? COLORS.highBg : COLORS.moderateBg}
        />
        <StatCard
          title="Conflicts Resolved"
          value={summary?.conflicts_detected || 0}
          subtitle="Deterministic tie-breaks"
          badge="RECONCILED"
          badgeColor={COLORS.conflict}
          badgeBg={COLORS.conflictBg}
        />
        <StatCard
          title="Out-of-Order"
          value={summary?.out_of_order_events || 0}
          subtitle="Reconstructed timelines"
          badge="REORDERED"
          badgeColor={COLORS.outOfOrder}
          badgeBg={COLORS.outOfOrderBg}
        />
        <StatCard
          title="Active Cameras"
          value={summary?.active_cameras || 0}
          subtitle="Optical sources"
        />
      </View>

      {/* Camera Health Section */}
      <View style={styles.sectionHeader}>
        <Text style={styles.sectionTitle}>Camera Fleet Reliability</Text>
      </View>
      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.horizontalScroll}>
        {cameras.map((cam) => (
          <CameraStatus key={cam.camera_id} camera={cam} />
        ))}
      </ScrollView>

      {/* Recent Conflicts Trace Preview */}
      {recentConflicts.length > 0 && (
        <>
          <View style={styles.sectionHeaderBetween}>
            <Text style={styles.sectionTitle}>Latest Conflict Resolutions</Text>
            <TouchableOpacity onPress={() => router.push('/conflicts')}>
              <Text style={styles.linkText}>View All Conflicts →</Text>
            </TouchableOpacity>
          </View>
          {recentConflicts.map((c) => (
            <DecisionTrace key={`conf-preview-${c.id}`} audit={c} />
          ))}
        </>
      )}

      {/* Top Students Preview */}
      <View style={styles.sectionHeaderBetween}>
        <Text style={styles.sectionTitle}>Student Engagement Roster</Text>
        <TouchableOpacity onPress={() => router.push('/students')}>
          <Text style={styles.linkText}>View Full Roster →</Text>
        </TouchableOpacity>
      </View>
      {students.slice(0, 5).map((stu) => (
        <StudentCard
          key={stu.id}
          student={stu}
          onPress={() => router.push(`/student/${stu.id}` as any)}
        />
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.bgApp,
  },
  contentContainer: {
    padding: SPACING.md,
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: SPACING.xl,
  },
  paddingContainer: {
    padding: SPACING.md,
  },
  loadingText: {
    marginTop: SPACING.md,
    color: COLORS.textMuted,
    fontSize: 14,
  },
  sectionHeader: {
    marginTop: SPACING.sm,
    marginBottom: SPACING.sm,
  },
  sectionHeaderBetween: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: SPACING.md,
    marginBottom: SPACING.sm,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: COLORS.textPrimary,
  },
  sectionSubtitle: {
    fontSize: 12,
    color: COLORS.textMuted,
    marginTop: 2,
  },
  linkText: {
    fontSize: 13,
    fontWeight: '600',
    color: COLORS.primary,
  },
  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginHorizontal: -SPACING.xs,
  },
  horizontalScroll: {
    marginBottom: SPACING.md,
  },
});
