import { useQuery } from 'react-query'
import { useState } from 'react'
import {
  School,
  Users,
  TrendingUp,
  Shield,
  CheckCircle2,
  Heart,
  GraduationCap,
  Activity,
} from 'lucide-react'
import apiClient from '../../api/client'
import NationalKPICard from '../../components/government/NationalKPICard'
import FilterBar from '../../components/government/FilterBar'
import StatisticalInsightCard from '../../components/government/StatisticalInsightCard'
import RegionalDistributionMap from '../../components/government/RegionalDistributionMap'
import SchoolTypeDistribution from '../../components/government/SchoolTypeDistribution'

export default function NationalOverview() {
  const [selectedRegions, setSelectedRegions] = useState<string[]>([])
  const [selectedSchoolTypes, setSelectedSchoolTypes] = useState<string[]>([])
  const [dateRange, setDateRange] = useState<{ start: Date | null; end: Date | null }>({
    start: null,
    end: null,
  })

  const regions = ['دبي', 'أبوظبي', 'الشارقة', 'عجمان', 'رأس الخيمة', 'الفجيرة', 'أم القيوين']
  const schoolTypes = ['حكومي', 'خاص', 'خاص ممول']

  const { data: overviewData, isLoading } = useQuery(
    'government-national-overview',
    async () => {
      try {
        const response = await apiClient.get('/government/national-overview', {
          params: {
            regions: selectedRegions.length > 0 ? selectedRegions : undefined,
            school_types: selectedSchoolTypes.length > 0 ? selectedSchoolTypes : undefined,
            start_date: dateRange.start?.toISOString(),
            end_date: dateRange.end?.toISOString(),
          },
        })
        return response.data
      } catch (error) {
        // Mock data for development
        return {
          kpis: {
            total_schools: 1247,
            total_schools_trend: 'up',
            total_schools_change: '+2.3%',
            active_students: 485230,
            active_students_trend: 'up',
            active_students_change: '+1.8%',
            avg_attendance: 94.2,
            avg_attendance_trend: 'up',
            avg_attendance_change: '+0.5%',
            system_health: 'healthy',
            safety_score: 96.8,
            safety_score_trend: 'neutral',
            safety_score_change: '0%',
            compliance_rate: 98.5,
            compliance_rate_trend: 'up',
            compliance_rate_change: '+0.2%',
            parent_engagement: 87.3,
            parent_engagement_trend: 'up',
            parent_engagement_change: '+1.2%',
            teacher_retention: 92.1,
            teacher_retention_trend: 'up',
            teacher_retention_change: '+0.8%',
          },
          regional_distribution: [
            { region: 'دبي', schools: 342, students: 142350, attendance: 95.2, safety: 97.1 },
            { region: 'أبوظبي', schools: 298, students: 128450, attendance: 94.8, safety: 96.9 },
            { region: 'الشارقة', schools: 187, students: 78420, attendance: 93.5, safety: 96.2 },
            { region: 'عجمان', schools: 98, students: 41230, attendance: 92.8, safety: 95.8 },
            { region: 'رأس الخيمة', schools: 156, students: 65420, attendance: 94.1, safety: 96.5 },
            { region: 'الفجيرة', schools: 87, students: 36210, attendance: 93.2, safety: 95.5 },
            { region: 'أم القيوين', schools: 79, students: 33150, attendance: 92.5, safety: 95.2 },
          ],
          school_type_distribution: [
            { type: 'حكومي', percentage: 65, schools: 810, students: 315400 },
            { type: 'خاص', percentage: 28, schools: 349, students: 135860 },
            { type: 'خاص ممول', percentage: 7, schools: 88, students: 33970 },
          ],
          insights: [
            {
              insight: 'زيادة 2.3% في عدد المدارس على أساس سنوي',
              insightEn: '2.3% increase in total schools YoY',
              type: 'positive' as const,
              supportingData: { 'المدارس الجديدة': '29', 'New Schools': '29' },
            },
            {
              insight: 'معدل الحضور مستقر عبر جميع المناطق',
              insightEn: 'Attendance rate stable across all regions',
              type: 'neutral' as const,
            },
            {
              insight: 'معدل الامتثال الأعلى في أبوظبي (99.1%)',
              insightEn: 'Highest compliance rate in Abu Dhabi (99.1%)',
              type: 'positive' as const,
            },
          ],
        }
      }
    },
    {
      refetchInterval: 300000, // Refresh every 5 minutes
    }
  )

  const kpis = overviewData?.kpis || {}
  const regionalData = overviewData?.regional_distribution || []
  const schoolTypeData = overviewData?.school_type_distribution || []
  const insights = overviewData?.insights || []

  const handleResetFilters = () => {
    setSelectedRegions([])
    setSelectedSchoolTypes([])
    setDateRange({ start: null, end: null })
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Filter Bar */}
      <FilterBar
        regions={regions}
        schoolTypes={schoolTypes}
        selectedRegions={selectedRegions}
        selectedSchoolTypes={selectedSchoolTypes}
        dateRange={dateRange}
        onRegionChange={setSelectedRegions}
        onSchoolTypeChange={setSelectedSchoolTypes}
        onDateRangeChange={setDateRange}
        onReset={handleResetFilters}
      />

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <NationalKPICard
          title="إجمالي المدارس"
          titleEn="Total Schools"
          value={kpis.total_schools?.toLocaleString() || '0'}
          trend={kpis.total_schools_trend}
          trendValue={kpis.total_schools_change}
          icon={School}
          color="emerald"
        />
        <NationalKPICard
          title="الطلاب النشطون"
          titleEn="Active Students"
          value={kpis.active_students?.toLocaleString() || '0'}
          trend={kpis.active_students_trend}
          trendValue={kpis.active_students_change}
          icon={Users}
          color="teal"
        />
        <NationalKPICard
          title="متوسط الحضور"
          titleEn="Average Attendance"
          value={`${kpis.avg_attendance?.toFixed(1) || '0'}%`}
          trend={kpis.avg_attendance_trend}
          trendValue={kpis.avg_attendance_change}
          icon={TrendingUp}
          color="emerald"
        />
        <NationalKPICard
          title="صحة النظام"
          titleEn="System Health"
          value={kpis.system_health === 'healthy' ? 'صحي / Healthy' : 'تحت المراقبة / Monitoring'}
          icon={Activity}
          color={kpis.system_health === 'healthy' ? 'emerald' : 'neutral'}
        />
        <NationalKPICard
          title="مؤشر السلامة"
          titleEn="Safety Score"
          value={`${kpis.safety_score?.toFixed(1) || '0'}%`}
          trend={kpis.safety_score_trend}
          trendValue={kpis.safety_score_change}
          icon={Shield}
          color="emerald"
        />
        <NationalKPICard
          title="معدل الامتثال"
          titleEn="Compliance Rate"
          value={`${kpis.compliance_rate?.toFixed(1) || '0'}%`}
          trend={kpis.compliance_rate_trend}
          trendValue={kpis.compliance_rate_change}
          icon={CheckCircle2}
          color="teal"
        />
        <NationalKPICard
          title="مشاركة أولياء الأمور"
          titleEn="Parent Engagement"
          value={`${kpis.parent_engagement?.toFixed(1) || '0'}%`}
          trend={kpis.parent_engagement_trend}
          trendValue={kpis.parent_engagement_change}
          icon={Heart}
          color="emerald"
        />
        <NationalKPICard
          title="استبقاء المعلمين"
          titleEn="Teacher Retention"
          value={`${kpis.teacher_retention?.toFixed(1) || '0'}%`}
          trend={kpis.teacher_retention_trend}
          trendValue={kpis.teacher_retention_change}
          icon={GraduationCap}
          color="teal"
        />
      </div>

      {/* Regional Distribution */}
      <div className="bg-white rounded-2xl p-6 border-2 border-gray-200 shadow-lg">
        <h2 className="text-xl font-bold text-gray-900 mb-2">التوزيع الإقليمي / Regional Distribution</h2>
        <p className="text-sm text-gray-500 mb-4">توزيع المدارس والطلاب حسب الإمارة</p>
        <RegionalDistributionMap data={regionalData} />
      </div>

      {/* School Type Distribution */}
      <div className="bg-white rounded-2xl p-6 border-2 border-gray-200 shadow-lg">
        <h2 className="text-xl font-bold text-gray-900 mb-2">توزيع أنواع المدارس / School Type Distribution</h2>
        <p className="text-sm text-gray-500 mb-4">نسبة المدارس حسب النوع</p>
        <SchoolTypeDistribution data={schoolTypeData} />
      </div>

      {/* Statistical Insights */}
      {insights.length > 0 && (
        <div className="space-y-3">
          <h2 className="text-xl font-bold text-gray-900">الرؤى الإحصائية / Statistical Insights</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {insights.map((insight: any, index: number) => (
              <StatisticalInsightCard
                key={index}
                insight={insight.insight}
                insightEn={insight.insightEn}
                type={insight.type}
                supportingData={insight.supportingData}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}


