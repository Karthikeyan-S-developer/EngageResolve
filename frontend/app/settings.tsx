import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Linking, Alert } from 'react-native';
import { ApiService } from '../services/api';
import { COLORS, THRESHOLDS, SPACING } from '../constants/theme';

export default function SettingsScreen() {
  const downloadEngagementCsv = () => {
    const url = ApiService.getEngagementCsvUrl();
    Linking.openURL(url).catch(() => Alert.alert('Export Link', `CSV Download URL: ${url}`));
  };

  const downloadAuditCsv = () => {
    const url = ApiService.getAuditCsvUrl();
    Linking.openURL(url).catch(() => Alert.alert('Export Link', `CSV Download URL: ${url}`));
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.title}>System Engine Configuration</Text>
        <Text style={styles.subtitle}>
          View deterministic resolution rules, camera reliability metrics, and Power BI export capabilities
        </Text>
      </View>

      {/* Identity Resolution Configuration */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Identity Resolution Engine</Text>
        <Text style={styles.cardSubtitle}>Spatio-temporal camera observation mapping thresholds</Text>

        <View style={styles.row}>
          <Text style={styles.label}>Temporal Window:</Text>
          <Text style={styles.val}>5.0 seconds</Text>
        </View>
        <View style={styles.row}>
          <Text style={styles.label}>Spatial Max Distance:</Text>
          <Text style={styles.val}>100 units</Text>
        </View>
        <View style={styles.row}>
          <Text style={styles.label}>Match Threshold Score:</Text>
          <Text style={styles.val}>0.70 (70%)</Text>
        </View>
        <View style={styles.row}>
          <Text style={styles.label}>Match Scoring Weights:</Text>
          <Text style={styles.val}>0.6 * Temporal + 0.4 * Spatial</Text>
        </View>
      </View>

      {/* Engagement Classification Thresholds */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Engagement Classification Rules</Text>
        <Text style={styles.cardSubtitle}>Domain status categorization boundaries</Text>

        <View style={styles.row}>
          <Text style={styles.label}>High Engagement:</Text>
          <Text style={[styles.val, { color: COLORS.high }]}>≥ {(THRESHOLDS.HIGH_ENGAGEMENT * 100).toFixed(0)}% (0.75)</Text>
        </View>
        <View style={styles.row}>
          <Text style={styles.label}>Moderate Engagement:</Text>
          <Text style={[styles.val, { color: COLORS.moderate }]}>0.45 – 0.74</Text>
        </View>
        <View style={styles.row}>
          <Text style={styles.label}>Low Engagement:</Text>
          <Text style={[styles.val, { color: COLORS.low }]}>&lt; {(THRESHOLDS.LOW_ENGAGEMENT * 100).toFixed(0)}% (0.45)</Text>
        </View>
      </View>

      {/* Camera Reliability Mapping Table */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Camera Reliability Table (Tie-Break Tier 5)</Text>
        <Text style={styles.cardSubtitle}>Configurable optical sensor trust weights</Text>

        <View style={styles.tableRow}>
          <Text style={styles.th}>Camera ID / Source</Text>
          <Text style={styles.th}>Reliability Score</Text>
        </View>
        <View style={styles.tableRow}>
          <Text style={styles.td}>front_camera / cam-01</Text>
          <Text style={styles.tdVal}>0.95 (95%)</Text>
        </View>
        <View style={styles.tableRow}>
          <Text style={styles.td}>side_camera / cam-02</Text>
          <Text style={styles.tdVal}>0.85 (85%)</Text>
        </View>
        <View style={styles.tableRow}>
          <Text style={styles.td}>rear_camera / cam-03</Text>
          <Text style={styles.tdVal}>0.80 (80%)</Text>
        </View>
        <View style={styles.tableRow}>
          <Text style={styles.td}>cam-04</Text>
          <Text style={styles.tdVal}>0.75 (75%)</Text>
        </View>
        <View style={styles.tableRow}>
          <Text style={styles.td}>Default Fallback</Text>
          <Text style={styles.tdVal}>0.70 (70%)</Text>
        </View>
      </View>

      {/* Power BI & Data Export */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Power BI CSV Data Exports</Text>
        <Text style={styles.cardSubtitle}>Generate clean CSV datasets suitable for Power BI analytics import</Text>

        <TouchableOpacity style={styles.exportBtn} onPress={downloadEngagementCsv}>
          <Text style={styles.exportBtnText}>📥 Export Engagement Timeline CSV</Text>
        </TouchableOpacity>

        <TouchableOpacity style={[styles.exportBtn, { marginTop: SPACING.sm }]} onPress={downloadAuditCsv}>
          <Text style={styles.exportBtnText}>📥 Export Audit Log CSV</Text>
        </TouchableOpacity>
      </View>
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
  },
  card: {
    backgroundColor: COLORS.bgSurface,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: COLORS.border,
    padding: SPACING.lg,
    marginBottom: SPACING.md,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: COLORS.textPrimary,
  },
  cardSubtitle: {
    fontSize: 12,
    color: COLORS.textMuted,
    marginTop: 2,
    marginBottom: SPACING.md,
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
  val: {
    fontSize: 13,
    fontWeight: '700',
    color: COLORS.textPrimary,
  },
  tableRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: SPACING.xs,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  th: {
    fontSize: 12,
    fontWeight: '700',
    color: COLORS.textMuted,
    textTransform: 'uppercase',
  },
  td: {
    fontSize: 13,
    color: COLORS.textPrimary,
  },
  tdVal: {
    fontSize: 13,
    fontWeight: '700',
    color: COLORS.primary,
  },
  exportBtn: {
    backgroundColor: COLORS.primaryLight,
    borderWidth: 1,
    borderColor: COLORS.primary,
    paddingVertical: SPACING.md,
    borderRadius: 6,
    alignItems: 'center',
  },
  exportBtnText: {
    fontSize: 14,
    fontWeight: '700',
    color: COLORS.primary,
  },
});
