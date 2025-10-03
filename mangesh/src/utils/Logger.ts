import { Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

export enum LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARN = 2,
  ERROR = 3,
}

interface LogEntry {
  timestamp: string;
  level: LogLevel;
  message: string;
  data?: any;
  stack?: string;
  userId?: string;
  sessionId?: string;
}

class Logger {
  private static instance: Logger;
  private logLevel: LogLevel = __DEV__ ? LogLevel.DEBUG : LogLevel.INFO;
  private maxLogEntries = 1000;
  private logs: LogEntry[] = [];

  private constructor() {
    this.initializeLogger();
  }

  public static getInstance(): Logger {
    if (!Logger.instance) {
      Logger.instance = new Logger();
    }
    return Logger.instance;
  }

  private async initializeLogger() {
    try {
      // Load existing logs from storage
      const storedLogs = await AsyncStorage.getItem('app_logs');
      if (storedLogs) {
        this.logs = JSON.parse(storedLogs);
      }
    } catch (error) {
      console.error('Failed to initialize logger:', error);
    }
  }

  private async saveLogs() {
    try {
      // Keep only the most recent logs
      if (this.logs.length > this.maxLogEntries) {
        this.logs = this.logs.slice(-this.maxLogEntries);
      }
      
      await AsyncStorage.setItem('app_logs', JSON.stringify(this.logs));
    } catch (error) {
      console.error('Failed to save logs:', error);
    }
  }

  private createLogEntry(level: LogLevel, message: string, data?: any, error?: Error): LogEntry {
    return {
      timestamp: new Date().toISOString(),
      level,
      message,
      data,
      stack: error?.stack,
      userId: 'current_user_id', // Get from user context
      sessionId: 'current_session_id', // Get from session context
    };
  }

  private log(level: LogLevel, message: string, data?: any, error?: Error) {
    const logEntry = this.createLogEntry(level, message, data, error);
    
    // Add to in-memory logs
    this.logs.push(logEntry);
    
    // Save to storage
    this.saveLogs();
    
    // Console output for development
    if (__DEV__) {
      const levelName = LogLevel[level];
      const timestamp = new Date().toLocaleTimeString();
      
      switch (level) {
        case LogLevel.DEBUG:
          console.log(`[${timestamp}] DEBUG: ${message}`, data);
          break;
        case LogLevel.INFO:
          console.info(`[${timestamp}] INFO: ${message}`, data);
          break;
        case LogLevel.WARN:
          console.warn(`[${timestamp}] WARN: ${message}`, data);
          break;
        case LogLevel.ERROR:
          console.error(`[${timestamp}] ERROR: ${message}`, data, error);
          break;
      }
    }
    
    // Send to remote logging service in production
    if (!__DEV__ && level >= LogLevel.ERROR) {
      this.sendToRemoteLogging(logEntry);
    }
  }

  private async sendToRemoteLogging(logEntry: LogEntry) {
    try {
      // Send to remote logging service (e.g., Sentry, LogRocket, etc.)
      // await RemoteLoggingService.sendLog(logEntry);
    } catch (error) {
      console.error('Failed to send log to remote service:', error);
    }
  }

  public debug(message: string, data?: any) {
    if (this.logLevel <= LogLevel.DEBUG) {
      this.log(LogLevel.DEBUG, message, data);
    }
  }

  public info(message: string, data?: any) {
    if (this.logLevel <= LogLevel.INFO) {
      this.log(LogLevel.INFO, message, data);
    }
  }

  public warn(message: string, data?: any) {
    if (this.logLevel <= LogLevel.WARN) {
      this.log(LogLevel.WARN, message, data);
    }
  }

  public error(message: string, error?: Error, data?: any) {
    this.log(LogLevel.ERROR, message, data, error);
  }

  public async getLogs(level?: LogLevel, limit?: number): Promise<LogEntry[]> {
    let filteredLogs = this.logs;
    
    if (level !== undefined) {
      filteredLogs = this.logs.filter(log => log.level >= level);
    }
    
    if (limit) {
      filteredLogs = filteredLogs.slice(-limit);
    }
    
    return filteredLogs;
  }

  public async clearLogs() {
    this.logs = [];
    await AsyncStorage.removeItem('app_logs');
  }

  public async exportLogs(): Promise<string> {
    return JSON.stringify(this.logs, null, 2);
  }

  public setLogLevel(level: LogLevel) {
    this.logLevel = level;
  }
}

// Export singleton instance
export const logger = Logger.getInstance();

// Convenience functions
export const logDebug = (message: string, data?: any) => logger.debug(message, data);
export const logInfo = (message: string, data?: any) => logger.info(message, data);
export const logWarn = (message: string, data?: any) => logger.warn(message, data);
export const logError = (message: string, error?: Error, data?: any) => logger.error(message, error, data);



