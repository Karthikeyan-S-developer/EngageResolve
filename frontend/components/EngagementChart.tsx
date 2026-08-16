import React from 'react';
import { View, Text, StyleSheet, LayoutChangeEvent } from 'react-native';
import Svg, { Line, Circle, Path, Rect, Text as SvgText } from 'react-native-svg';
import { COLORS, THRESHOLDS, SPACING } from '../constants/theme';
import { TimelineItem } from '../services/types';

interface EngagementChartProps {
  timeline: TimelineItem[];
  height?: number;
  onSelectPoint?: (item: TimelineItem) => void;
  selectedPoint?: TimelineItem | null;
}

export const EngagementChart: React.FC<EngagementChartProps> = ({
  timeline,
  height = 240,
  onSelectPoint,
  selectedPoint,
}) => {
  const [containerWidth, setContainerWidth] = React.useState<number>(600);

  const handleLayout = (event: LayoutChangeEvent) => {
    const { width } = event.nativeEvent.layout;
    if (width > 0) {
      setContainerWidth(width);
    }
  };

  if (!timeline || timeline.length === 0) {
    return (
      <View style={[styles.container, { height }]}>
        <Text style={styles.emptyText}>No timeline observation states available.</Text>
      </View>
    );
  }

  const paddingLeft = 45;
  const paddingRight = 20;
  const paddingTop = 20;
  const paddingBottom = 35;

  const chartWidth = Math.max(containerWidth - paddingLeft - paddingRight, 100);
  const chartHeight = height - paddingTop - paddingBottom;

  // Calculate coordinates for points
  const points = timeline.map((item, idx) => {
    const x = paddingLeft + (idx / Math.max(timeline.length - 1, 1)) * chartWidth;
    const y = paddingTop + (1 - Math.max(0, Math.min(1, item.engagement_score))) * chartHeight;
    return { x, y, item };
  });

  // Construct SVG Path String
  let pathD = '';
  points.forEach((pt, idx) => {
    if (idx === 0) {
      pathD += `M ${pt.x} ${pt.y}`;
    } else {
      pathD += ` L ${pt.x} ${pt.y}`;
    }
  });

  // Y-Axis Threshold Positions
  const yHigh = paddingTop + (1 - THRESHOLDS.HIGH_ENGAGEMENT) * chartHeight;
  const yLow = paddingTop + (1 - THRESHOLDS.LOW_ENGAGEMENT) * chartHeight;

  return (
    <View style={styles.container} onLayout={handleLayout}>
      <Svg width={containerWidth} height={height}>
        {/* Background Grid Lines & Threshold Labels */}
        <Line x1={paddingLeft} y1={paddingTop} x2={containerWidth - paddingRight} y2={paddingTop} stroke={COLORS.border} strokeDasharray="3 3" />
        <SvgText x={paddingLeft - 8} y={paddingTop + 4} fill={COLORS.textMuted} fontSize="10" textAnchor="end">1.00</SvgText>

        {/* High Engagement Threshold Line (0.75) */}
        <Line x1={paddingLeft} y1={yHigh} x2={containerWidth - paddingRight} y2={yHigh} stroke={COLORS.high} strokeWidth="1.5" strokeDasharray="4 4" opacity={0.6} />
        <SvgText x={paddingLeft - 8} y={yHigh + 4} fill={COLORS.high} fontSize="10" textAnchor="end">0.75</SvgText>

        {/* Low Engagement Threshold Line (0.45) */}
        <Line x1={paddingLeft} y1={yLow} x2={containerWidth - paddingRight} y2={yLow} stroke={COLORS.low} strokeWidth="1.5" strokeDasharray="4 4" opacity={0.6} />
        <SvgText x={paddingLeft - 8} y={yLow + 4} fill={COLORS.low} fontSize="10" textAnchor="end">0.45</SvgText>

        {/* Bottom Line */}
        <Line x1={paddingLeft} y1={paddingTop + chartHeight} x2={containerWidth - paddingRight} y2={paddingTop + chartHeight} stroke={COLORS.border} />
        <SvgText x={paddingLeft - 8} y={paddingTop + chartHeight + 4} fill={COLORS.textMuted} fontSize="10" textAnchor="end">0.00</SvgText>

        {/* Timeline Path Line */}
        {pathD ? <Path d={pathD} stroke={COLORS.primary} strokeWidth="2.5" fill="none" /> : null}

        {/* Data Point Circles */}
        {points.map((pt, idx) => {
          const isSelected = selectedPoint?.version === pt.item.version;
          const pointColor = pt.item.engagement_score >= 0.75 ? COLORS.high : (pt.item.engagement_score < 0.45 ? COLORS.low : COLORS.moderate);

          // Format x-axis timestamp (HH:MM:SS)
          const timeStr = pt.item.effective_timestamp.includes('T')
            ? pt.item.effective_timestamp.split('T')[1].replace('Z', '')
            : pt.item.effective_timestamp;

          return (
            <React.Fragment key={`point-${idx}`}>
              {/* X Axis Time Labels for subset of points */}
              {(idx === 0 || idx === points.length - 1 || idx % Math.ceil(points.length / 5) === 0) && (
                <SvgText
                  x={pt.x}
                  y={height - 10}
                  fill={COLORS.textMuted}
                  fontSize="10"
                  textAnchor="middle"
                >
                  {timeStr}
                </SvgText>
              )}

              {/* Touch/Click Target & Dot */}
              <Circle
                cx={pt.x}
                cy={pt.y}
                r={isSelected ? 7 : 5}
                fill={pointColor}
                stroke={isSelected ? COLORS.bgSurface : COLORS.bgSurface}
                strokeWidth={2}
                onPress={() => onSelectPoint && onSelectPoint(pt.item)}
              />
            </React.Fragment>
          );
        })}
      </Svg>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.bgSurface,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: COLORS.border,
    paddingVertical: SPACING.sm,
    justifyContent: 'center',
    alignItems: 'center',
    width: '100%',
  },
  emptyText: {
    color: COLORS.textMuted,
    fontSize: 14,
  },
});
