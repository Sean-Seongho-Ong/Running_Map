/**
 * 로깅 유틸리티
 * 
 * 규칙 10에 따라 print() 사용 금지, 로깅 라이브러리 사용 필수
 * 개발 환경과 프로덕션 환경을 구분하여 로깅 레벨 관리
 */

type LogLevel = 'DEBUG' | 'INFO' | 'WARN' | 'ERROR' | 'FATAL';

interface LogEntry {
  timestamp: string;
  level: LogLevel;
  module: string;
  message: string;
  data?: unknown;
}

class Logger {
  private module: string;
  private isDevelopment: boolean;

  constructor(module: string) {
    this.module = module;
    this.isDevelopment = __DEV__ || process.env.NODE_ENV === 'development';
  }

  private formatMessage(level: LogLevel, message: string, data?: unknown): LogEntry {
    return {
      timestamp: new Date().toISOString(),
      level,
      module: this.module,
      message,
      ...(data && { data }),
    };
  }

  private log(level: LogLevel, message: string, data?: unknown): void {
    // 프로덕션 환경에서는 DEBUG 로그 비활성화 (규칙 10)
    if (!this.isDevelopment && level === 'DEBUG') {
      return;
    }

    const logEntry = this.formatMessage(level, message, data);

    // 개발 환경에서는 console 사용 (React Native 제약)
    // 프로덕션에서는 로그 수집 서비스로 전송 가능
    switch (level) {
      case 'DEBUG':
        if (this.isDevelopment) {
          console.debug(`[${logEntry.level}] [${logEntry.module}] ${logEntry.message}`, data || '');
        }
        break;
      case 'INFO':
        console.info(`[${logEntry.level}] [${logEntry.module}] ${logEntry.message}`, data || '');
        break;
      case 'WARN':
        console.warn(`[${logEntry.level}] [${logEntry.module}] ${logEntry.message}`, data || '');
        break;
      case 'ERROR':
      case 'FATAL':
        console.error(`[${logEntry.level}] [${logEntry.module}] ${logEntry.message}`, data || '');
        break;
    }
  }

  debug(message: string, data?: unknown): void {
    this.log('DEBUG', message, data);
  }

  info(message: string, data?: unknown): void {
    this.log('INFO', message, data);
  }

  warn(message: string, data?: unknown): void {
    this.log('WARN', message, data);
  }

  error(message: string, data?: unknown): void {
    this.log('ERROR', message, data);
  }

  fatal(message: string, data?: unknown): void {
    this.log('FATAL', message, data);
  }
}

/**
 * 로거 인스턴스 생성
 * @param module 모듈명 (파일 경로 또는 모듈 이름)
 */
export function createLogger(module: string): Logger {
  return new Logger(module);
}

/**
 * 기본 로거 (전역 사용)
 */
export const logger = createLogger('App');

