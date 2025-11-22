/**
 * App Entry Point
 * Expo Bare Workflow
 */

import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { AppNavigator } from './src/interface/navigation/AppNavigator';

export default function App() {
  return (
    <>
      <AppNavigator />
      <StatusBar style="auto" />
    </>
  );
}

