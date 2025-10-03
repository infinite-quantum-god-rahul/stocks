import { logInfo, logError } from '../utils/Logger';
import { AnalyticsService } from './AnalyticsService';

export interface SubscriptionPlan {
  id: string;
  name: string;
  price: number;
  currency: string;
  duration: 'monthly' | 'yearly';
  features: string[];
  maxJobApplications: number;
  prioritySupport: boolean;
  advancedMatching: boolean;
  premiumInsights: boolean;
  customProfile: boolean;
  directMessaging: boolean;
  interviewScheduling: boolean;
  salaryNegotiation: boolean;
  careerCoaching: boolean;
}

export interface RevenueStream {
  id: string;
  name: string;
  type: 'subscription' | 'commission' | 'advertising' | 'premium_features' | 'data_insights';
  revenue: number;
  conversionRate: number;
  averageValue: number;
  monthlyActiveUsers: number;
}

export interface UserTier {
  id: string;
  name: string;
  level: number;
  benefits: string[];
  requirements: {
    minApplications?: number;
    minMatches?: number;
    minRating?: number;
    minTimeActive?: number;
  };
  rewards: {
    bonusApplications?: number;
    priorityMatching?: boolean;
    exclusiveJobs?: boolean;
    premiumSupport?: boolean;
  };
}

class MonetizationService {
  private static instance: MonetizationService;
  private subscriptionPlans: SubscriptionPlan[] = [];
  private revenueStreams: RevenueStream[] = [];
  private userTiers: UserTier[] = [];

  private constructor() {
    this.initializeService();
  }

  public static getInstance(): MonetizationService {
    if (!MonetizationService.instance) {
      MonetizationService.instance = new MonetizationService();
    }
    return MonetizationService.instance;
  }

  private async initializeService() {
    try {
      this.initializeSubscriptionPlans();
      this.initializeRevenueStreams();
      this.initializeUserTiers();
      logInfo('MonetizationService initialized successfully');
    } catch (error) {
      logError('Failed to initialize MonetizationService', error);
    }
  }

  private initializeSubscriptionPlans() {
    this.subscriptionPlans = [
      {
        id: 'free',
        name: 'Free',
        price: 0,
        currency: 'USD',
        duration: 'monthly',
        features: [
          'Basic job matching',
          '5 job applications per month',
          'Standard profile',
          'Email support'
        ],
        maxJobApplications: 5,
        prioritySupport: false,
        advancedMatching: false,
        premiumInsights: false,
        customProfile: false,
        directMessaging: false,
        interviewScheduling: false,
        salaryNegotiation: false,
        careerCoaching: false,
      },
      {
        id: 'premium',
        name: 'Premium',
        price: 29.99,
        currency: 'USD',
        duration: 'monthly',
        features: [
          'Advanced AI matching',
          'Unlimited job applications',
          'Priority support',
          'Premium insights',
          'Custom profile',
          'Direct messaging',
          'Interview scheduling',
          'Salary negotiation tips'
        ],
        maxJobApplications: -1, // Unlimited
        prioritySupport: true,
        advancedMatching: true,
        premiumInsights: true,
        customProfile: true,
        directMessaging: true,
        interviewScheduling: true,
        salaryNegotiation: true,
        careerCoaching: false,
      },
      {
        id: 'pro',
        name: 'Pro',
        price: 49.99,
        currency: 'USD',
        duration: 'monthly',
        features: [
          'Everything in Premium',
          'Personal career coach',
          'Exclusive job opportunities',
          'Advanced analytics',
          'Custom resume builder',
          'LinkedIn optimization',
          'Interview preparation',
          'Salary benchmarking'
        ],
        maxJobApplications: -1,
        prioritySupport: true,
        advancedMatching: true,
        premiumInsights: true,
        customProfile: true,
        directMessaging: true,
        interviewScheduling: true,
        salaryNegotiation: true,
        careerCoaching: true,
      },
      {
        id: 'enterprise',
        name: 'Enterprise',
        price: 99.99,
        currency: 'USD',
        duration: 'monthly',
        features: [
          'Everything in Pro',
          'Team collaboration',
          'Bulk applications',
          'Custom integrations',
          'Dedicated account manager',
          'White-label options',
          'Advanced reporting',
          'API access'
        ],
        maxJobApplications: -1,
        prioritySupport: true,
        advancedMatching: true,
        premiumInsights: true,
        customProfile: true,
        directMessaging: true,
        interviewScheduling: true,
        salaryNegotiation: true,
        careerCoaching: true,
      }
    ];
  }

  private initializeRevenueStreams() {
    this.revenueStreams = [
      {
        id: 'subscription_revenue',
        name: 'Subscription Revenue',
        type: 'subscription',
        revenue: 0,
        conversionRate: 0.15, // 15% conversion rate
        averageValue: 39.99,
        monthlyActiveUsers: 0,
      },
      {
        id: 'commission_revenue',
        name: 'Commission Revenue',
        type: 'commission',
        revenue: 0,
        conversionRate: 0.05, // 5% commission on successful placements
        averageValue: 2500, // Average commission per placement
        monthlyActiveUsers: 0,
      },
      {
        id: 'premium_features',
        name: 'Premium Features',
        type: 'premium_features',
        revenue: 0,
        conversionRate: 0.08, // 8% conversion to premium features
        averageValue: 19.99,
        monthlyActiveUsers: 0,
      },
      {
        id: 'data_insights',
        name: 'Data Insights',
        type: 'data_insights',
        revenue: 0,
        conversionRate: 0.02, // 2% conversion to data insights
        averageValue: 99.99,
        monthlyActiveUsers: 0,
      },
      {
        id: 'advertising_revenue',
        name: 'Advertising Revenue',
        type: 'advertising',
        revenue: 0,
        conversionRate: 0.12, // 12% click-through rate
        averageValue: 2.50, // Average revenue per click
        monthlyActiveUsers: 0,
      }
    ];
  }

  private initializeUserTiers() {
    this.userTiers = [
      {
        id: 'bronze',
        name: 'Bronze',
        level: 1,
        benefits: [
          'Basic job matching',
          'Standard profile',
          'Email support'
        ],
        requirements: {
          minApplications: 0,
          minMatches: 0,
          minRating: 0,
          minTimeActive: 0
        },
        rewards: {
          bonusApplications: 0,
          priorityMatching: false,
          exclusiveJobs: false,
          premiumSupport: false
        }
      },
      {
        id: 'silver',
        name: 'Silver',
        level: 2,
        benefits: [
          'Enhanced job matching',
          'Priority in search results',
          'Basic insights',
          'Chat support'
        ],
        requirements: {
          minApplications: 10,
          minMatches: 5,
          minRating: 4.0,
          minTimeActive: 30
        },
        rewards: {
          bonusApplications: 5,
          priorityMatching: true,
          exclusiveJobs: false,
          premiumSupport: false
        }
      },
      {
        id: 'gold',
        name: 'Gold',
        level: 3,
        benefits: [
          'Advanced AI matching',
          'Exclusive job opportunities',
          'Premium insights',
          'Priority support',
          'Interview scheduling'
        ],
        requirements: {
          minApplications: 25,
          minMatches: 15,
          minRating: 4.5,
          minTimeActive: 90
        },
        rewards: {
          bonusApplications: 15,
          priorityMatching: true,
          exclusiveJobs: true,
          premiumSupport: true
        }
      },
      {
        id: 'platinum',
        name: 'Platinum',
        level: 4,
        benefits: [
          'Everything in Gold',
          'Personal career coach',
          'Custom profile optimization',
          'Advanced analytics',
          'Direct company access'
        ],
        requirements: {
          minApplications: 50,
          minMatches: 30,
          minRating: 4.8,
          minTimeActive: 180
        },
        rewards: {
          bonusApplications: 30,
          priorityMatching: true,
          exclusiveJobs: true,
          premiumSupport: true
        }
      }
    ];
  }

  public async getSubscriptionPlans(): Promise<SubscriptionPlan[]> {
    return this.subscriptionPlans;
  }

  public async getSubscriptionPlan(planId: string): Promise<SubscriptionPlan | null> {
    return this.subscriptionPlans.find(plan => plan.id === planId) || null;
  }

  public async calculateRevenueProjection(months: number = 12): Promise<{
    totalRevenue: number;
    monthlyBreakdown: number[];
    revenueStreams: { [key: string]: number };
  }> {
    try {
      const monthlyBreakdown: number[] = [];
      const revenueStreams: { [key: string]: number } = {};
      let totalRevenue = 0;

      for (let month = 1; month <= months; month++) {
        let monthlyRevenue = 0;

        // Calculate growth factor (assuming 10% monthly growth)
        const growthFactor = Math.pow(1.1, month - 1);

        for (const stream of this.revenueStreams) {
          const streamRevenue = stream.averageValue * stream.conversionRate * stream.monthlyActiveUsers * growthFactor;
          monthlyRevenue += streamRevenue;
          
          if (!revenueStreams[stream.id]) {
            revenueStreams[stream.id] = 0;
          }
          revenueStreams[stream.id] += streamRevenue;
        }

        monthlyBreakdown.push(monthlyRevenue);
        totalRevenue += monthlyRevenue;
      }

      logInfo(`Revenue projection calculated for ${months} months: $${totalRevenue.toFixed(2)}`);
      
      return {
        totalRevenue,
        monthlyBreakdown,
        revenueStreams
      };
    } catch (error) {
      logError('Failed to calculate revenue projection', error);
      throw error;
    }
  }

  public async optimizePricing(userId: string, currentPlan: string): Promise<{
    recommendedPlan: string;
    reasons: string[];
    potentialSavings: number;
    additionalRevenue: number;
  }> {
    try {
      // Analyze user behavior and suggest optimal pricing
      const userMetrics = await this.getUserMetrics(userId);
      const currentPlanData = await this.getSubscriptionPlan(currentPlan);
      
      if (!currentPlanData) {
        throw new Error('Current plan not found');
      }

      let recommendedPlan = currentPlan;
      const reasons: string[] = [];
      let potentialSavings = 0;
      let additionalRevenue = 0;

      // Analyze usage patterns
      if (userMetrics.applicationsPerMonth > currentPlanData.maxJobApplications && currentPlanData.maxJobApplications !== -1) {
        // User is exceeding their plan limits
        const premiumPlan = await this.getSubscriptionPlan('premium');
        if (premiumPlan) {
          recommendedPlan = 'premium';
          reasons.push('You\'re exceeding your monthly application limit');
          additionalRevenue = premiumPlan.price - currentPlanData.price;
        }
      }

      if (userMetrics.matchesPerMonth > 20 && currentPlan === 'free') {
        // High-performing user on free plan
        const premiumPlan = await this.getSubscriptionPlan('premium');
        if (premiumPlan) {
          recommendedPlan = 'premium';
          reasons.push('You\'re getting great matches - upgrade for unlimited applications');
          additionalRevenue = premiumPlan.price;
        }
      }

      if (userMetrics.supportTickets > 3 && currentPlan === 'free') {
        // User needs more support
        const premiumPlan = await this.getSubscriptionPlan('premium');
        if (premiumPlan) {
          recommendedPlan = 'premium';
          reasons.push('Get priority support with Premium');
          additionalRevenue = premiumPlan.price;
        }
      }

      // Calculate potential savings for yearly plans
      if (currentPlan !== 'free') {
        const yearlyPlan = await this.getSubscriptionPlan(currentPlan + '_yearly');
        if (yearlyPlan) {
          const monthlyCost = currentPlanData.price * 12;
          const yearlyCost = yearlyPlan.price;
          if (yearlyCost < monthlyCost) {
            potentialSavings = monthlyCost - yearlyCost;
            reasons.push(`Save $${potentialSavings.toFixed(2)} with yearly billing`);
          }
        }
      }

      AnalyticsService.trackEvent('pricing_optimization_suggested', {
        userId,
        currentPlan,
        recommendedPlan,
        potentialSavings,
        additionalRevenue
      });

      return {
        recommendedPlan,
        reasons,
        potentialSavings,
        additionalRevenue
      };
    } catch (error) {
      logError('Failed to optimize pricing', error);
      throw error;
    }
  }

  private async getUserMetrics(userId: string): Promise<{
    applicationsPerMonth: number;
    matchesPerMonth: number;
    supportTickets: number;
    timeActive: number;
    rating: number;
  }> {
    // In a real app, this would fetch from your analytics/usage data
    return {
      applicationsPerMonth: 8,
      matchesPerMonth: 15,
      supportTickets: 1,
      timeActive: 45, // days
      rating: 4.7
    };
  }

  public async getUserTier(userId: string): Promise<UserTier> {
    try {
      const userMetrics = await this.getUserMetrics(userId);
      
      // Find the highest tier the user qualifies for
      for (let i = this.userTiers.length - 1; i >= 0; i--) {
        const tier = this.userTiers[i];
        if (
          userMetrics.applicationsPerMonth >= (tier.requirements.minApplications || 0) &&
          userMetrics.matchesPerMonth >= (tier.requirements.minMatches || 0) &&
          userMetrics.rating >= (tier.requirements.minRating || 0) &&
          userMetrics.timeActive >= (tier.requirements.minTimeActive || 0)
        ) {
          return tier;
        }
      }
      
      return this.userTiers[0]; // Return bronze tier as default
    } catch (error) {
      logError('Failed to get user tier', error);
      return this.userTiers[0];
    }
  }

  public async trackRevenue(event: string, value: number, userId?: string): Promise<void> {
    try {
      // Track revenue events for analytics
      AnalyticsService.trackEvent('revenue_event', {
        event,
        value,
        userId,
        timestamp: new Date().toISOString()
      });

      logInfo(`Revenue event tracked: ${event} - $${value}`);
    } catch (error) {
      logError('Failed to track revenue event', error);
    }
  }

  public async getRevenueAnalytics(period: 'daily' | 'weekly' | 'monthly' | 'yearly'): Promise<{
    totalRevenue: number;
    revenueGrowth: number;
    topRevenueStreams: { name: string; revenue: number; percentage: number }[];
    conversionRates: { [key: string]: number };
  }> {
    try {
      // In a real app, this would fetch from your analytics database
      const mockData = {
        totalRevenue: 125000,
        revenueGrowth: 0.15, // 15% growth
        topRevenueStreams: [
          { name: 'Subscription Revenue', revenue: 75000, percentage: 60 },
          { name: 'Commission Revenue', revenue: 30000, percentage: 24 },
          { name: 'Premium Features', revenue: 15000, percentage: 12 },
          { name: 'Data Insights', revenue: 5000, percentage: 4 }
        ],
        conversionRates: {
          free_to_premium: 0.15,
          premium_to_pro: 0.08,
          pro_to_enterprise: 0.03
        }
      };

      logInfo(`Revenue analytics retrieved for period: ${period}`);
      return mockData;
    } catch (error) {
      logError('Failed to get revenue analytics', error);
      throw error;
    }
  }
}

export const monetizationService = MonetizationService.getInstance();



