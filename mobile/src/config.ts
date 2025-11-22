import { Platform } from 'react-native';

// Android Emulator uses 10.0.2.2 to access localhost of the host machine
// iOS Simulator uses localhost
const API_URL = Platform.select({
  android: 'http://10.0.2.2:8000/api/v1',
  ios: 'http://localhost:8000/api/v1',
  default: 'http://localhost:8000/api/v1',
});

export const config = {
  API_BASE_URL: API_URL,
  TIMEOUT: 10000, // 10 seconds
};
