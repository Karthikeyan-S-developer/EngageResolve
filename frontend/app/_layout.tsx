import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, SafeAreaView } from 'react-native';
import { Slot, useRouter, usePathname } from 'expo-router';
import { DashboardHeader } from '../components/DashboardHeader';
import { COLORS, SPACING } from '../constants/theme';

export default function RootLayout() {
  const router = useRouter();
  const pathname = usePathname();

  const navItems = [
    { label: 'Dashboard', path: '/' },
    { label: 'Students', path: '/students' },
    { label: 'Replay Simulator', path: '/replay' },
    { label: 'Audit Trail', path: '/audit' },
    { label: 'Conflicts Inspector', path: '/conflicts' },
    { label: 'Settings', path: '/settings' },
  ];

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.container}>
        <DashboardHeader />

        {/* Enterprise Navigation Bar */}
        <View style={styles.navBar}>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.navScroll}>
            {navItems.map((item) => {
              const isActive = pathname === item.path || (item.path !== '/' && pathname.startsWith(item.path));
              return (
                <TouchableOpacity
                  key={item.path}
                  style={[styles.navTab, isActive && styles.navTabActive]}
                  onPress={() => router.push(item.path as any)}
                >
                  <Text style={[styles.navText, isActive && styles.navTextActive]}>
                    {item.label}
                  </Text>
                </TouchableOpacity>
              );
            })}
          </ScrollView>
        </View>

        {/* Page View Slot */}
        <View style={styles.content}>
          <Slot />
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: COLORS.bgHeader,
  },
  container: {
    flex: 1,
    backgroundColor: COLORS.bgApp,
  },
  navBar: {
    backgroundColor: COLORS.bgHeader,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.borderDark,
  },
  navScroll: {
    paddingHorizontal: SPACING.md,
  },
  navTab: {
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm + 2,
    marginRight: SPACING.xs,
    borderBottomWidth: 3,
    borderBottomColor: 'transparent',
  },
  navTabActive: {
    borderBottomColor: COLORS.primary,
  },
  navText: {
    fontSize: 13,
    fontWeight: '600',
    color: COLORS.textMuted,
  },
  navTextActive: {
    color: COLORS.textInverse,
    fontWeight: '700',
  },
  content: {
    flex: 1,
  },
});
