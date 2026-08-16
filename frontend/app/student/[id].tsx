import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, ActivityIndicator, TouchableOpacity } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { ApiService } from '../../services/api';
import { StudentProfile, TimelineItem, AuditLog } from '../../services/types';
import { StatCard } from '../../components/StatCard';
import { EngagementBadge } from '../../components/EngagementBadge';
import { EngagementChart } from '../../components/EngagementChart';
import { EventTimeline } from '../../components/EventTimeline';
import { AuditPanel } from '../../components/AuditPanel';
import { EmptyState } from '../../components/EmptyState';
import { COLORS, SPACING } from '../../constants/theme';

export default function StudentDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState<StudentProfile | null>(null);
  const [timeline, setTimeline] = useState<TimelineItem[]>([]);
  const [audits, setAudits] = useState<AuditLog[]>([]);
  const [activeTab, setActiveTab] = useState<'timeline' | 'audit'>('timeline');
  const [selectedPoint, setSelectedPoint] = useState<TimelineItem | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadStudentData = async () => {
    if (!id) return;
    try {
      setLoading(true);
      setError(null);
      const [profRes, timeRes, auditRes] = await Promise.all([
        ApiService.getStudentProfile(id),
        ApiService.getStudentTimeline(id),
        ApiService.getStudentAudit(id),
      ]);
      setProfile(profRes);
      setTimeline(timeRes.timeline || []);
      setAudits(auditRes.audit_logs || []);
    } catch (err: any) {
      setError(err.message || `Failed to load student profile for ${id}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStudentData();
  }, [id]);

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={COLORS.primary} />
        <Text style={styles.loadingText}>Loading student profile...</Text>
      </View>
    );
  }

  if (error || !profile) {
    return (
      <View style={styles.padding}>
        <EmptyState title="Student Profile Error" message={error || 'Profile not found.'} onRetry={loadStudentData} />
      </View>
    );
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Header Profile Info */}
      <View style={styles.profileHeader}>
        <TouchableOpacity style={styles.backBtn} onPress={() => router.back()}>
          <Text style={styles.backBtnText}>← Back to Roster</Text>
        </TouchableOpacity>

        <View style={styles.titleRow}>
          <View>
            <Text style={styles.name}>{profile.display_name}</Text>
            <Text style={styles.studentId}>Canonical ID: {profile.id}</Text>
          </View>
          <EngagementBadge score={profile.current_engagement} />
        </View>

        <View style={styles.kpiRow}>
          <StatCard title="Current Score" value={`${(profile.current_engagement * 100).toFixed(0)}%`} />
          <StatCard title="Average Score" value={`${(profile.average_engagement * 100).toFixed(0)}%`} />
          <StatCard title="Highest Score" value={`${(profile.highest_engagement * 100).toFixed(0)}%`} />
          <StatCard title="Lowest Score" value={`${(profile.lowest_engagement * 100).toFixed(0)}%`} />
          <StatCard title="State Versions" value={profile.state_versions_count} />
          <StatCard title="Conflicts" value={profile.conflicts_count} badgeColor={COLORS.conflict} badgeBg={COLORS.conflictBg} />
        </View>
      </View>

      {/* Main Time-Series Visualization */}
      <View style={styles.chartBox}>
        <View style={styles.chartHeader}>
          <Text style={styles.chartTitle}>Reconstructed Engagement Timeline</Text>

          {selectedPoint && (
            <Text style={styles.selectedDetail}>
              Selected: Version {selectedPoint.version} ({(selectedPoint.engagement_score * 100).toFixed(0)}%)
            </Text>
          )}
        </View>

        <EngagementChart
          timeline={timeline}
          onSelectPoint={(item) => setSelectedPoint(item)}
          selectedPoint={selectedPoint}
        />
      </View>

      {/* Sub-View Tabs: Timeline vs Audit */}
      <View style={styles.tabContainer}>
        <TouchableOpacity
          style={[styles.tab, activeTab === 'timeline' && styles.tabActive]}
          onPress={() => setActiveTab('timeline')}
        >
          <Text style={[styles.tabText, activeTab === 'timeline' && styles.tabTextActive]}>
            Versioned Event Timeline ({timeline.length})
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.tab, activeTab === 'audit' && styles.tabActive]}
          onPress={() => setActiveTab('audit')}
        >
          <Text style={[styles.tabText, activeTab === 'audit' && styles.tabTextActive]}>
            Audit & Decision Traces ({audits.length})
          </Text>
        </TouchableOpacity>
      </View>

      {activeTab === 'timeline' ? (
        <EventTimeline
          timeline={timeline}
          selectedVersion={selectedPoint?.version}
          onSelectVersion={(item) => setSelectedPoint(item)}
        />
      ) : (
        <AuditPanel audits={audits} />
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
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  padding: {
    padding: SPACING.md,
  },
  loadingText: {
    marginTop: SPACING.md,
    color: COLORS.textMuted,
    fontSize: 14,
  },
  profileHeader: {
    backgroundColor: COLORS.bgSurface,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: COLORS.border,
    padding: SPACING.md,
    marginBottom: SPACING.md,
  },
  backBtn: {
    marginBottom: SPACING.sm,
  },
  backBtnText: {
    fontSize: 13,
    fontWeight: '600',
    color: COLORS.primary,
  },
  titleRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: SPACING.md,
  },
  name: {
    fontSize: 22,
    fontWeight: '800',
    color: COLORS.textPrimary,
  },
  studentId: {
    fontSize: 12,
    color: COLORS.textMuted,
    marginTop: 2,
  },
  kpiRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginHorizontal: -SPACING.xs,
  },
  chartBox: {
    marginBottom: SPACING.md,
  },
  chartHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  chartTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: COLORS.textPrimary,
  },
  selectedDetail: {
    fontSize: 12,
    fontWeight: '700',
    color: COLORS.primary,
  },
  tabContainer: {
    flexDirection: 'row',
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
    marginBottom: SPACING.sm,
  },
  tab: {
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.md,
    borderBottomWidth: 3,
    borderBottomColor: 'transparent',
    marginRight: SPACING.sm,
  },
  tabActive: {
    borderBottomColor: COLORS.primary,
  },
  tabText: {
    fontSize: 13,
    fontWeight: '600',
    color: COLORS.textMuted,
  },
  tabTextActive: {
    color: COLORS.textPrimary,
    fontWeight: '700',
  },
});
