import { logInfo, logError } from '../utils/Logger';
import { AnalyticsService } from './AnalyticsService';

export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  salary: {
    min: number;
    max: number;
    currency: string;
  };
  description: string;
  requirements: string[];
  skills: string[];
  experience: {
    min: number;
    max: number;
  };
  type: 'full-time' | 'part-time' | 'contract' | 'internship';
  remote: boolean;
  benefits: string[];
  postedDate: string;
  applicationDeadline?: string;
  industry: string;
  companySize: 'startup' | 'small' | 'medium' | 'large' | 'enterprise';
  companyRating?: number;
  logo?: string;
}

export interface UserProfile {
  id: string;
  name: string;
  email: string;
  skills: string[];
  experience: number;
  education: {
    degree: string;
    field: string;
    institution: string;
    year: number;
  }[];
  workHistory: {
    company: string;
    position: string;
    duration: number;
    description: string;
  }[];
  preferences: {
    salary: {
      min: number;
      max: number;
    };
    location: string[];
    jobTypes: string[];
    remote: boolean;
    industries: string[];
    companySize: string[];
  };
  achievements: string[];
  certifications: string[];
  languages: string[];
  availability: 'immediate' | '2-weeks' | '1-month' | '3-months';
}

export interface MatchResult {
  job: Job;
  matchScore: number;
  reasons: string[];
  strengths: string[];
  improvements: string[];
  salaryMatch: boolean;
  locationMatch: boolean;
  skillsMatch: number;
  experienceMatch: boolean;
}

class JobMatchingService {
  private static instance: JobMatchingService;
  private jobs: Job[] = [];
  private userProfiles: Map<string, UserProfile> = new Map();

  private constructor() {
    this.initializeService();
  }

  public static getInstance(): JobMatchingService {
    if (!JobMatchingService.instance) {
      JobMatchingService.instance = new JobMatchingService();
    }
    return JobMatchingService.instance;
  }

  private async initializeService() {
    try {
      await this.loadJobs();
      logInfo('JobMatchingService initialized successfully');
    } catch (error) {
      logError('Failed to initialize JobMatchingService', error);
    }
  }

  private async loadJobs() {
    try {
      // In a real app, this would load from API
      // For now, we'll use mock data
      this.jobs = await this.getMockJobs();
    } catch (error) {
      logError('Failed to load jobs', error);
      throw error;
    }
  }

  private async getMockJobs(): Promise<Job[]> {
    // Mock job data - in production, this would come from your API
    return [
      {
        id: '1',
        title: 'Senior React Native Developer',
        company: 'TechCorp',
        location: 'San Francisco, CA',
        salary: { min: 120000, max: 180000, currency: 'USD' },
        description: 'We are looking for a senior React Native developer...',
        requirements: ['React Native', 'TypeScript', 'Redux', '5+ years experience'],
        skills: ['React Native', 'TypeScript', 'JavaScript', 'Redux', 'Firebase'],
        experience: { min: 5, max: 10 },
        type: 'full-time',
        remote: true,
        benefits: ['Health Insurance', '401k', 'Flexible Hours'],
        postedDate: '2024-01-15',
        industry: 'Technology',
        companySize: 'large',
        companyRating: 4.5,
      },
      // Add more mock jobs...
    ];
  }

  public async getJobMatches(userId: string, limit: number = 20): Promise<MatchResult[]> {
    try {
      const userProfile = this.userProfiles.get(userId);
      if (!userProfile) {
        throw new Error('User profile not found');
      }

      const matches: MatchResult[] = [];

      for (const job of this.jobs) {
        const matchResult = this.calculateMatch(userProfile, job);
        if (matchResult.matchScore > 0.3) { // Only include matches above 30%
          matches.push(matchResult);
        }
      }

      // Sort by match score (highest first)
      matches.sort((a, b) => b.matchScore - a.matchScore);

      // Limit results
      const limitedMatches = matches.slice(0, limit);

      // Track analytics
      AnalyticsService.trackEvent('job_matches_generated', {
        userId,
        totalMatches: matches.length,
        returnedMatches: limitedMatches.length,
        averageScore: limitedMatches.reduce((sum, match) => sum + match.matchScore, 0) / limitedMatches.length,
      });

      logInfo(`Generated ${limitedMatches.length} job matches for user ${userId}`);
      return limitedMatches;
    } catch (error) {
      logError('Failed to get job matches', error);
      throw error;
    }
  }

  private calculateMatch(userProfile: UserProfile, job: Job): MatchResult {
    let totalScore = 0;
    let maxScore = 0;
    const reasons: string[] = [];
    const strengths: string[] = [];
    const improvements: string[] = [];

    // Skills matching (40% weight)
    const skillsMatch = this.calculateSkillsMatch(userProfile.skills, job.skills);
    totalScore += skillsMatch.score * 0.4;
    maxScore += 0.4;
    if (skillsMatch.score > 0.7) {
      strengths.push(`Strong match in ${skillsMatch.matchedSkills.join(', ')}`);
    } else if (skillsMatch.score < 0.3) {
      improvements.push(`Consider learning: ${skillsMatch.missingSkills.join(', ')}`);
    }
    reasons.push(`Skills match: ${Math.round(skillsMatch.score * 100)}%`);

    // Experience matching (25% weight)
    const experienceMatch = this.calculateExperienceMatch(userProfile.experience, job.experience);
    totalScore += experienceMatch * 0.25;
    maxScore += 0.25;
    if (experienceMatch > 0.8) {
      strengths.push('Experience level matches perfectly');
    } else if (experienceMatch < 0.5) {
      improvements.push('Gain more experience in this field');
    }
    reasons.push(`Experience match: ${Math.round(experienceMatch * 100)}%`);

    // Salary matching (20% weight)
    const salaryMatch = this.calculateSalaryMatch(userProfile.preferences.salary, job.salary);
    totalScore += salaryMatch * 0.2;
    maxScore += 0.2;
    if (salaryMatch > 0.8) {
      strengths.push('Salary expectations align well');
    } else if (salaryMatch < 0.5) {
      improvements.push('Consider adjusting salary expectations');
    }
    reasons.push(`Salary match: ${Math.round(salaryMatch * 100)}%`);

    // Location matching (10% weight)
    const locationMatch = this.calculateLocationMatch(userProfile.preferences.location, job.location, job.remote);
    totalScore += locationMatch * 0.1;
    maxScore += 0.1;
    if (locationMatch > 0.8) {
      strengths.push('Location preferences match');
    } else if (locationMatch < 0.5) {
      improvements.push('Consider remote work or relocation');
    }
    reasons.push(`Location match: ${Math.round(locationMatch * 100)}%`);

    // Job type matching (5% weight)
    const jobTypeMatch = this.calculateJobTypeMatch(userProfile.preferences.jobTypes, job.type);
    totalScore += jobTypeMatch * 0.05;
    maxScore += 0.05;
    reasons.push(`Job type match: ${Math.round(jobTypeMatch * 100)}%`);

    const finalScore = maxScore > 0 ? totalScore / maxScore : 0;

    return {
      job,
      matchScore: finalScore,
      reasons,
      strengths,
      improvements,
      salaryMatch: salaryMatch > 0.7,
      locationMatch: locationMatch > 0.7,
      skillsMatch: skillsMatch.score,
      experienceMatch: experienceMatch > 0.7,
    };
  }

  private calculateSkillsMatch(userSkills: string[], jobSkills: string[]): {
    score: number;
    matchedSkills: string[];
    missingSkills: string[];
  } {
    const userSkillsLower = userSkills.map(skill => skill.toLowerCase());
    const jobSkillsLower = jobSkills.map(skill => skill.toLowerCase());
    
    const matchedSkills = jobSkillsLower.filter(skill => 
      userSkillsLower.some(userSkill => 
        userSkill.includes(skill) || skill.includes(userSkill)
      )
    );
    
    const missingSkills = jobSkillsLower.filter(skill => 
      !userSkillsLower.some(userSkill => 
        userSkill.includes(skill) || skill.includes(userSkill)
      )
    );

    const score = jobSkills.length > 0 ? matchedSkills.length / jobSkills.length : 0;

    return {
      score,
      matchedSkills: matchedSkills.map(skill => 
        jobSkills[jobSkillsLower.indexOf(skill)]
      ),
      missingSkills: missingSkills.map(skill => 
        jobSkills[jobSkillsLower.indexOf(skill)]
      ),
    };
  }

  private calculateExperienceMatch(userExperience: number, jobExperience: { min: number; max: number }): number {
    if (userExperience >= jobExperience.min && userExperience <= jobExperience.max) {
      return 1.0; // Perfect match
    } else if (userExperience > jobExperience.max) {
      return 0.8; // Overqualified but still good
    } else if (userExperience >= jobExperience.min * 0.8) {
      return 0.6; // Close to minimum requirement
    } else {
      return 0.2; // Underqualified
    }
  }

  private calculateSalaryMatch(userSalary: { min: number; max: number }, jobSalary: { min: number; max: number; currency: string }): number {
    const userMid = (userSalary.min + userSalary.max) / 2;
    const jobMid = (jobSalary.min + jobSalary.max) / 2;
    
    if (userMid >= jobSalary.min && userMid <= jobSalary.max) {
      return 1.0; // Perfect match
    } else if (userMid < jobSalary.min) {
      return 0.3; // Below minimum
    } else {
      return 0.7; // Above maximum but acceptable
    }
  }

  private calculateLocationMatch(userLocations: string[], jobLocation: string, isRemote: boolean): number {
    if (isRemote) {
      return 1.0; // Remote work matches any location
    }
    
    const jobLocationLower = jobLocation.toLowerCase();
    const userLocationsLower = userLocations.map(loc => loc.toLowerCase());
    
    const hasMatch = userLocationsLower.some(userLoc => 
      jobLocationLower.includes(userLoc) || userLoc.includes(jobLocationLower)
    );
    
    return hasMatch ? 1.0 : 0.0;
  }

  private calculateJobTypeMatch(userJobTypes: string[], jobType: string): number {
    return userJobTypes.includes(jobType) ? 1.0 : 0.0;
  }

  public async saveUserProfile(userId: string, profile: UserProfile): Promise<void> {
    try {
      this.userProfiles.set(userId, profile);
      logInfo(`User profile saved for user ${userId}`);
    } catch (error) {
      logError('Failed to save user profile', error);
      throw error;
    }
  }

  public async getUserProfile(userId: string): Promise<UserProfile | null> {
    return this.userProfiles.get(userId) || null;
  }

  public async getJobById(jobId: string): Promise<Job | null> {
    return this.jobs.find(job => job.id === jobId) || null;
  }

  public async searchJobs(query: string, filters?: {
    location?: string;
    salary?: { min: number; max: number };
    experience?: { min: number; max: number };
    jobType?: string;
    remote?: boolean;
  }): Promise<Job[]> {
    try {
      let filteredJobs = this.jobs;

      // Text search
      if (query) {
        const queryLower = query.toLowerCase();
        filteredJobs = filteredJobs.filter(job =>
          job.title.toLowerCase().includes(queryLower) ||
          job.company.toLowerCase().includes(queryLower) ||
          job.description.toLowerCase().includes(queryLower) ||
          job.skills.some(skill => skill.toLowerCase().includes(queryLower))
        );
      }

      // Apply filters
      if (filters) {
        if (filters.location) {
          filteredJobs = filteredJobs.filter(job =>
            job.location.toLowerCase().includes(filters.location!.toLowerCase()) ||
            job.remote
          );
        }

        if (filters.salary) {
          filteredJobs = filteredJobs.filter(job =>
            job.salary.max >= filters.salary!.min &&
            job.salary.min <= filters.salary!.max
          );
        }

        if (filters.experience) {
          filteredJobs = filteredJobs.filter(job =>
            job.experience.max >= filters.experience!.min &&
            job.experience.min <= filters.experience!.max
          );
        }

        if (filters.jobType) {
          filteredJobs = filteredJobs.filter(job => job.type === filters.jobType);
        }

        if (filters.remote !== undefined) {
          filteredJobs = filteredJobs.filter(job => job.remote === filters.remote);
        }
      }

      logInfo(`Job search completed: ${filteredJobs.length} results for query "${query}"`);
      return filteredJobs;
    } catch (error) {
      logError('Failed to search jobs', error);
      throw error;
    }
  }
}

export const jobMatchingService = JobMatchingService.getInstance();



