/**
 * AppNavigator
 * Bottom Tab + Stack Navigator 구조
 */

import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { useTheme } from '../hooks/useTheme';
import { MapScreen } from '../screens/MapScreen';
import { CourseListScreen } from '../screens/CourseListScreen';
import { CourseGenerationScreen } from '../screens/CourseGenerationScreen';
import { RunningScreen } from '../screens/RunningScreen';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

// Map Stack
const MapStack = () => (
  <Stack.Navigator>
    <Stack.Screen
      name="Map"
      component={MapScreen}
      options={{ headerShown: false }}
    />
    <Stack.Screen
      name="CourseGeneration"
      component={CourseGenerationScreen}
      options={{ title: '코스 생성' }}
    />
  </Stack.Navigator>
);

// Courses Stack
const CoursesStack = () => (
  <Stack.Navigator>
    <Stack.Screen
      name="CourseList"
      component={CourseListScreen}
      options={{ title: '내 코스' }}
    />
  </Stack.Navigator>
);

// Running Stack
const RunningStack = () => (
  <Stack.Navigator>
    <Stack.Screen
      name="Running"
      component={RunningScreen}
      options={{ headerShown: false }}
    />
  </Stack.Navigator>
);

export const AppNavigator = () => {
  const theme = useTheme();
  
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={{
          tabBarActiveTintColor: theme.colors.primary,
          tabBarInactiveTintColor: theme.colors.textSecondary,
          headerStyle: {
            backgroundColor: theme.colors.surface,
          },
          headerTintColor: theme.colors.text,
          tabBarStyle: {
            backgroundColor: theme.colors.surface,
            borderTopColor: theme.colors.border,
          },
        }}
      >
        <Tab.Screen
          name="MapTab"
          component={MapStack}
          options={{
            title: '지도',
            tabBarLabel: '지도',
            headerShown: false,
          }}
        />
        <Tab.Screen
          name="CoursesTab"
          component={CoursesStack}
          options={{
            title: '코스',
            tabBarLabel: '코스',
          }}
        />
        <Tab.Screen
          name="RunningTab"
          component={RunningStack}
          options={{
            title: '러닝',
            tabBarLabel: '러닝',
            headerShown: false,
          }}
        />
      </Tab.Navigator>
    </NavigationContainer>
  );
};

