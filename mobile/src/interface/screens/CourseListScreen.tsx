/**
 * CourseListScreen
 * 코스 목록 화면
 */

import React, { useEffect, useState } from 'react';
import { View, StyleSheet, FlatList, Text } from 'react-native';
import { Input } from '../components/common/Input';
import { Card } from '../components/common/Card';
import { Loading } from '../components/common/Loading';
import { useTheme } from '../hooks/useTheme';
import { useCourseStore } from '../store/courseStore';
import { Course } from '../../domain/entities/Course';
import { Theme } from '../../theme';

export const CourseListScreen: React.FC = () => {
  const theme = useTheme();
  const styles = createStyles(theme);
  const { courses, loadCourses, selectCourse } = useCourseStore();
  const [searchQuery, setSearchQuery] = useState('');
  
  useEffect(() => {
    loadCourses();
  }, []);
  
  const filteredCourses = courses.filter(course =>
    course.name?.toLowerCase().includes(searchQuery.toLowerCase())
  );
  
  const handleCoursePress = (course: Course) => {
    selectCourse(course.id);
    // TODO: 코스 상세 화면으로 이동
  };
  
  const renderCourseItem = ({ item }: { item: Course }) => (
    <Card
      style={styles.courseCard}
      onPress={() => handleCoursePress(item)}
      elevated
    >
      <Text style={styles.courseName}>{item.name || '이름 없음'}</Text>
      <Text style={styles.courseDistance}>
        거리: {item.distance.kilometers.toFixed(2)} km
      </Text>
      <Text style={styles.courseDate}>
        생성일: {item.createdAt.toLocaleDateString()}
      </Text>
    </Card>
  );
  
  return (
    <View style={styles.container}>
      <View style={styles.searchContainer}>
        <Input
          placeholder="코스 검색..."
          value={searchQuery}
          onChangeText={setSearchQuery}
          containerStyle={styles.searchInput}
        />
      </View>
      {filteredCourses.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyText}>저장된 코스가 없습니다.</Text>
        </View>
      ) : (
        <FlatList
          data={filteredCourses}
          renderItem={renderCourseItem}
          keyExtractor={(item) => item.id}
          contentContainerStyle={styles.listContainer}
        />
      )}
    </View>
  );
};

const createStyles = (theme: Theme) =>
  StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: theme.colors.background,
    },
    searchContainer: {
      padding: theme.spacing.md,
      backgroundColor: theme.colors.surface,
    },
    searchInput: {
      marginBottom: 0,
    },
    listContainer: {
      padding: theme.spacing.md,
    },
    courseCard: {
      marginBottom: theme.spacing.md,
    },
    courseName: {
      ...theme.typography.h3,
      color: theme.colors.text,
      marginBottom: theme.spacing.xs,
    },
    courseDistance: {
      ...theme.typography.body,
      color: theme.colors.textSecondary,
      marginBottom: theme.spacing.xs,
    },
    courseDate: {
      ...theme.typography.caption,
      color: theme.colors.textSecondary,
    },
    emptyContainer: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
    },
    emptyText: {
      ...theme.typography.body,
      color: theme.colors.textSecondary,
    },
  });

