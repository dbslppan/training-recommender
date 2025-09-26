#!/usr/bin/env python3
"""
Training Recommendation System - Streamlit Interface
A complete web application for employee training recommendations based on competency assessments.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
from typing import Dict, List, Tuple, Optional

# Page configuration
st.set_page_config(
    page_title="🎯 Training Recommendation System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .priority-critical {
        background-color: #ff4444;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-weight: bold;
    }
    .priority-high {
        background-color: #ff8800;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-weight: bold;
    }
    .priority-medium {
        background-color: #2196F3;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-weight: bold;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    .training-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        background: white;
    }
</style>
""", unsafe_allow_html=True)


class TrainingRecommendationSystem:
    """Complete Training Recommendation System with Streamlit Integration"""
    
    def __init__(self):
        self.setup_competency_mapping()
        self.setup_division_mapping()
        self.setup_training_database()
        self.setup_ui_data()
    
    def setup_competency_mapping(self):
        """Setup competency to training mapping matrix"""
        self.competency_training_mapping = {
            'core_information_seeking': ['Teknologi Informasi', 'Strategi SDM'],
            'core_resilience': ['SDM', 'Program Keahlian Khusus'],
            'core_achievement_orientation': ['Strategi SDM', 'Financial Management for Leader'],
            'core_concern_for_order': ['Audit Internal & Manajemen Risiko', 'Akuntansi & Keuangan'],
            'core_organizational_commitment': ['SDM', 'Strategi SDM'],
            'core_ethical_oriented': ['Hukum', 'Audit Internal dan Manajemen Risiko'],
            
            'managerial_building_collaborative_relationship': ['SDM', 'Strategi Pemasaran'],
            'managerial_business_savvy': ['Agribusiness Productivity Institute', 'Strategi SDM'],
            'managerial_customer_focus': ['Strategi Pemasaran', 'Agribusiness Productivity Institute'],
            'managerial_strategic_orientation': ['Transformasi Strategis', 'Strategi Transfrormasi'],
            'managerial_sustainability_mindset': ['Operasional Tanaman Tebu (On Farm)', 'Operasional Tanaman Sawit (On Farm)'],
            'managerial_execution_focused': ['Operasional Pabrik Kelapa Sawit (Off Farm)', 'Operasional Tanaman Karet (On Farm)'],
            'managerial_digital_literate': ['Teknologi Informasi', 'Transformasi Strategis'],
            
            'leadership_creativity_innovation': ['Transformasi Strategis', 'Strategi Transfrormasi'],
            'leadership_transformational_leadership': ['SDM', 'Strategi SDM'],
            'leadership_nurturing_empowering_people': ['SDM', 'Program Keahlian Khusus'],
            'leadership_managing_equality_diversity': ['SDM', 'Hukum']
        }
    
    def setup_division_mapping(self):
        """Setup division to training school mapping"""
        self.division_mapping = {
            'plantation': ['Operasional Tanaman', 'Agribusiness Productivity Institute'],
            'factory': ['Operasional Pabrik'],
            'finance': ['Akuntansi & Keuangan', 'Financial Management'],
            'hr': ['SDM', 'Strategi SDM'],
            'it': ['Teknologi Informasi'],
            'procurement': ['Pengadaan'],
            'audit': ['Audit Internal'],
            'legal': ['Hukum'],
            'strategy': ['Transformasi Strategis', 'Strategi'],
            'marketing': ['Strategi Pemasaran']
        }
    
    def setup_training_database(self):
        """Setup comprehensive training database"""
        self.training_database = {
            # PLANTATION DIVISION
            'PL-2024-418': {
                'training_name': 'PENDEKATAN LOGIKA MENGIDENTIFIKASI ANOMALI PRODUKSI',
                'school': 'Agribusiness Productivity Institute',
                'target_division': 'plantation',
                'target_level': 'ALL',
                'duration_days': 3,
                'cost': 6000000,
                'job_family': 'Tanaman',
                'learning_objectives': [
                    'Integrasi geospike dan lingkungan di perkebunan',
                    'Seasonal effect di tanaman sawit', 
                    'Prinsip dasar pemahaman data produksi',
                    'Metode identifikasi anomali di perkebunan'
                ]
            },
            'PL-2024-P0153': {
                'training_name': 'Budidaya Tanaman Tebu - Persiapan Lahan & Kultivasi',
                'school': 'Operasional Tanaman Tebu (On Farm)',
                'target_division': 'plantation',
                'target_level': 'Operasional',
                'duration_days': 5,
                'cost': 5000000,
                'job_family': 'Tanaman',
                'learning_objectives': [
                    'Teknik dasar kultivasi tebu',
                    'Manajemen pengairan dan irigasi',
                    'Pengendalian OPT tebu',
                    'Sustainable farming practices'
                ]
            },
            'PL-2024-P0154': {
                'training_name': 'Operasional Tanaman Sawit - Advanced Plantation Management',
                'school': 'Operasional Tanaman Sawit (On Farm)',
                'target_division': 'plantation',
                'target_level': 'Manager',
                'duration_days': 4,
                'cost': 7500000,
                'job_family': 'Tanaman',
                'learning_objectives': [
                    'Advanced plantation management techniques',
                    'Yield optimization strategies',
                    'Team leadership in plantation operations',
                    'Environmental sustainability practices'
                ]
            },
            # FACTORY DIVISION
            'FC-2024-201': {
                'training_name': 'Operasional Pabrik Kelapa Sawit - Process Optimization',
                'school': 'Operasional Pabrik Kelapa Sawit (Off Farm)',
                'target_division': 'factory',
                'target_level': 'ALL',
                'duration_days': 6,
                'cost': 8000000,
                'job_family': 'Pabrik',
                'learning_objectives': [
                    'Advanced palm oil processing techniques',
                    'Quality control and assurance',
                    'Equipment maintenance and optimization',
                    'Safety protocols and procedures'
                ]
            },
            'FC-2024-202': {
                'training_name': 'Manufacturing Excellence & Lean Production',
                'school': 'Operasional Pabrik Kelapa Sawit (Off Farm)',
                'target_division': 'factory',
                'target_level': 'Supervisor',
                'duration_days': 4,
                'cost': 6500000,
                'job_family': 'Pabrik',
                'learning_objectives': [
                    'Lean manufacturing principles',
                    'Continuous improvement methodologies',
                    'Team leadership in manufacturing',
                    'Waste reduction techniques'
                ]
            },
            # FINANCE DIVISION
            'FN-2024-301': {
                'training_name': 'Financial Management for Leaders',
                'school': 'Financial Management for Leader (Jakarta)',
                'target_division': 'finance',
                'target_level': 'Manager',
                'duration_days': 5,
                'cost': 9000000,
                'job_family': 'Keuangan',
                'learning_objectives': [
                    'Strategic financial planning',
                    'Investment analysis and decision making',
                    'Financial risk management',
                    'Budget planning and control',
                    'Leadership in finance function'
                ]
            },
            'FN-2024-302': {
                'training_name': 'Advanced Accounting & Financial Reporting',
                'school': 'Akuntansi & Keuangan',
                'target_division': 'finance',
                'target_level': 'ALL',
                'duration_days': 4,
                'cost': 5500000,
                'job_family': 'Keuangan',
                'learning_objectives': [
                    'Advanced accounting principles',
                    'Financial reporting standards',
                    'Digital accounting systems',
                    'Compliance and regulatory requirements'
                ]
            },
            # HR DIVISION
            'HR-2024-401': {
                'training_name': 'Strategic Human Resource Management',
                'school': 'SDM',
                'target_division': 'hr',
                'target_level': 'Manager',
                'duration_days': 5,
                'cost': 7000000,
                'job_family': 'SDM',
                'learning_objectives': [
                    'Strategic HR planning and execution',
                    'Talent management and development',
                    'Employee engagement strategies',
                    'Performance management systems',
                    'Diversity and inclusion practices'
                ]
            },
            'HR-2024-402': {
                'training_name': 'Employee Development & Training Design',
                'school': 'Program Keahlian Khusus',
                'target_division': 'hr',
                'target_level': 'ALL',
                'duration_days': 4,
                'cost': 5000000,
                'job_family': 'SDM',
                'learning_objectives': [
                    'Training needs analysis',
                    'Learning program design',
                    'Adult learning principles',
                    'Training evaluation methods'
                ]
            },
            # IT DIVISION
            'IT-2024-501': {
                'training_name': 'Digital Transformation & Technology Leadership',
                'school': 'Teknologi Informasi',
                'target_division': 'it',
                'target_level': 'Manager',
                'duration_days': 6,
                'cost': 10000000,
                'job_family': 'IT',
                'learning_objectives': [
                    'Digital transformation strategies',
                    'IT governance and management',
                    'Emerging technology evaluation',
                    'Cybersecurity leadership',
                    'Innovation management in IT'
                ]
            },
            'IT-2024-502': {
                'training_name': 'Information Systems & Data Analytics',
                'school': 'Teknologi Informasi',
                'target_division': 'it',
                'target_level': 'ALL',
                'duration_days': 5,
                'cost': 7500000,
                'job_family': 'IT',
                'learning_objectives': [
                    'Database design and management',
                    'Data analytics and visualization',
                    'Business intelligence systems',
                    'System integration techniques'
                ]
            },
            # PROCUREMENT DIVISION
            'PR-2024-601': {
                'training_name': 'Strategic Procurement & Supply Chain Management',
                'school': 'Pengadaan',
                'target_division': 'procurement',
                'target_level': 'Manager',
                'duration_days': 5,
                'cost': 8000000,
                'job_family': 'Pengadaan',
                'learning_objectives': [
                    'Strategic sourcing methodologies',
                    'Supplier relationship management',
                    'Contract negotiation and management',
                    'Supply chain optimization',
                    'Risk management in procurement'
                ]
            },
            'PR-2024-602': {
                'training_name': 'Procurement Operations & Vendor Management',
                'school': 'Pengadaan',
                'target_division': 'procurement',
                'target_level': 'ALL',
                'duration_days': 4,
                'cost': 5500000,
                'job_family': 'Pengadaan',
                'learning_objectives': [
                    'Procurement processes and procedures',
                    'Vendor evaluation and selection',
                    'Cost analysis and budgeting',
                    'Compliance and ethics in procurement'
                ]
            },
            # AUDIT DIVISION
            'AD-2024-701': {
                'training_name': 'Internal Audit & Risk Management Leadership',
                'school': 'Audit Internal & Manajemen Risiko',
                'target_division': 'audit',
                'target_level': 'Manager',
                'duration_days': 6,
                'cost': 9500000,
                'job_family': 'Audit',
                'learning_objectives': [
                    'Advanced internal auditing techniques',
                    'Enterprise risk management',
                    'Audit leadership and team management',
                    'Regulatory compliance frameworks',
                    'Fraud detection and prevention'
                ]
            },
            'AD-2024-702': {
                'training_name': 'Risk Assessment & Control Systems',
                'school': 'Audit Internal dan Manajemen Risiko',
                'target_division': 'audit',
                'target_level': 'ALL',
                'duration_days': 4,
                'cost': 6000000,
                'job_family': 'Audit',
                'learning_objectives': [
                    'Risk identification and assessment',
                    'Internal control evaluation',
                    'Audit documentation and reporting',
                    'Technology-assisted audit techniques'
                ]
            },
            # LEGAL DIVISION
            'LG-2024-801': {
                'training_name': 'Corporate Law & Regulatory Compliance',
                'school': 'Hukum',
                'target_division': 'legal',
                'target_level': 'ALL',
                'duration_days': 5,
                'cost': 7500000,
                'job_family': 'Hukum',
                'learning_objectives': [
                    'Corporate governance principles',
                    'Regulatory compliance management',
                    'Contract law and negotiations',
                    'Employment law and regulations',
                    'Business ethics and compliance'
                ]
            },
            # STRATEGY & TRANSFORMATION DIVISION
            'ST-2024-901': {
                'training_name': 'Strategic Transformation & Change Management',
                'school': 'Transformasi Strategis',
                'target_division': 'strategy',
                'target_level': 'Manager',
                'duration_days': 7,
                'cost': 12000000,
                'job_family': 'Strategi',
                'learning_objectives': [
                    'Strategic planning and execution',
                    'Change management methodologies',
                    'Digital transformation strategies',
                    'Innovation management',
                    'Organizational development'
                ]
            },
            'ST-2024-902': {
                'training_name': 'Marketing Strategy & Customer Excellence',
                'school': 'Strategi Pemasaran',
                'target_division': 'marketing',
                'target_level': 'ALL',
                'duration_days': 4,
                'cost': 6500000,
                'job_family': 'Pemasaran',
                'learning_objectives': [
                    'Market analysis and segmentation',
                    'Customer relationship management',
                    'Brand management and positioning',
                    'Digital marketing strategies'
                ]
            },
            # GENERAL MANAGEMENT
            'GM-2024-001': {
                'training_name': 'Executive Leadership Development Program',
                'school': 'Strategi SDM',
                'target_division': 'ALL',
                'target_level': 'Senior Manager',
                'duration_days': 10,
                'cost': 15000000,
                'job_family': 'Umum',
                'learning_objectives': [
                    'Executive leadership skills',
                    'Strategic thinking and planning',
                    'Organizational transformation',
                    'High-performance team building',
                    'Stakeholder management',
                    'Innovation and change leadership'
                ]
            }
        }
    
    def setup_ui_data(self):
        """Setup data for UI components"""
        self.competency_labels = {
            # Core Competencies
            'information_seeking': 'Information Seeking',
            'resilience': 'Resilience',
            'achievement_orientation': 'Achievement Orientation',
            'concern_for_order': 'Concern for Order',
            'organizational_commitment': 'Organizational Commitment',
            'ethical_oriented': 'Ethical Oriented',
            
            # Managerial Competencies
            'building_collaborative_relationship': 'Building Collaborative Relationship',
            'business_savvy': 'Business Savvy',
            'customer_focus': 'Customer Focus',
            'strategic_orientation': 'Strategic Orientation',
            'sustainability_mindset': 'Sustainability Mindset',
            'execution_focused': 'Execution Focused',
            'digital_literate': 'Digital Literate',
            
            # Leadership Competencies
            'creativity_innovation': 'Creativity & Innovation',
            'transformational_leadership': 'Transformational Leadership',
            'nurturing_empowering_people': 'Nurturing and Empowering People',
            'managing_equality_diversity': 'Managing Equality & Diversity'
        }
        
        self.divisions = ['plantation', 'factory', 'finance', 'hr', 'it', 'procurement', 'audit', 'legal', 'strategy', 'marketing']
        self.positions = ['Staff', 'Senior Staff', 'Supervisor', 'Assistant Manager', 'Manager', 'Senior Manager', 'General Manager']
        self.experience_levels = ['junior', 'mid', 'senior']
    
    def identify_priority_areas(self, assessment_data: Dict) -> List[Tuple[str, float]]:
        """Identify priority competency areas based on assessment scores"""
        all_scores = {}
        
        # Safely combine all scores with category prefix
        core_scores = assessment_data.get('core_competency_scores', {})
        for competency, score in core_scores.items():
            all_scores[f'core_{competency}'] = float(score)
        
        managerial_scores = assessment_data.get('managerial_competency_scores', {})
        for competency, score in managerial_scores.items():
            all_scores[f'managerial_{competency}'] = float(score)
            
        leadership_scores = assessment_data.get('leadership_competency_scores', {})
        for competency, score in leadership_scores.items():
            all_scores[f'leadership_{competency}'] = float(score)
        
        # Sort by score (ascending - lowest first)
        priority_areas = sorted(all_scores.items(), key=lambda x: x[1])
        return priority_areas[:5]  # Top 5 priority areas
    
    def get_priority_level(self, score: float) -> int:
        """Determine priority level based on competency score"""
        if score < 2.0:
            return 1  # Critical - Immediate training needed
        elif score < 3.0:
            return 2  # High - Training needed within 3 months
        elif score < 3.5:
            return 3  # Medium - Training needed within 6 months
        else:
            return 4  # Low - Optional development
    
    def is_management_training(self, training_name: str) -> bool:
        """Check if training is suitable for management positions"""
        if not training_name:
            return False
        mgmt_keywords = ['strategi', 'leadership', 'management', 'manajemen', 'strategic', 'executive']
        return any(keyword in training_name.lower() for keyword in mgmt_keywords)
    
    def is_advanced_training(self, training_name: str) -> bool:
        """Check if training is advanced level"""
        if not training_name:
            return False
        advanced_keywords = ['advanced', 'strategic', 'transformasi', 'leadership', 'executive']
        return any(keyword in training_name.lower() for keyword in advanced_keywords)
    
    def filter_by_context(self, trainings: List[str], position: str, division: str, experience: str) -> List[str]:
        """Filter trainings based on employee context"""
        filtered = list(trainings)  # Start with all trainings
        
        # Position-based filtering
        if 'manager' in position.lower() or 'supervisor' in position.lower():
            # Keep management-suitable trainings
            management_keywords = ['strategic', 'leadership', 'management', 'manajemen', 'transformasi']
            management_trainings = [t for t in trainings if any(keyword in t.lower() for keyword in management_keywords)]
            filtered.extend(management_trainings)
        
        # Division-based filtering
        division_trainings = self.division_mapping.get(division.lower(), [])
        if division_trainings:
            division_matches = [t for t in trainings if any(dt.lower() in t.lower() for dt in division_trainings)]
            filtered.extend(division_matches)
        
        # Experience-based filtering
        if experience.lower() == 'junior':
            # Remove advanced trainings for junior employees
            advanced_keywords = ['advanced', 'strategic', 'transformasi', 'executive']
            filtered = [t for t in filtered if not any(keyword in t.lower() for keyword in advanced_keywords)]
        elif experience.lower() == 'senior':
            # Add strategic trainings for senior employees
            strategic_trainings = [t for t in trainings if any(keyword in t.lower() for keyword in ['strategic', 'leadership', 'transformasi'])]
            filtered.extend(strategic_trainings)
        
        # Remove duplicates and return
        return list(set(filtered))
    
    def calculate_relevance_score(self, competency: str, current_score: float, 
                                training_details: Dict, employee_data: Dict) -> float:
        """Calculate relevance score for a training recommendation"""
        base_score = 5.0 - current_score  # Lower current score = higher relevance
        
        # Contextual multipliers
        position_multiplier = 1.0
        current_position = employee_data.get('current_position', '').lower()
        if 'manager' in current_position or 'supervisor' in current_position:
            if self.is_management_training(training_details.get('training_name', '')):
                position_multiplier = 1.5
        
        division_multiplier = 1.0
        target_division = training_details.get('target_division', '').lower()
        employee_division = employee_data.get('division', '').lower()
        if target_division == employee_division or target_division == 'all':
            division_multiplier = 1.3
        
        experience_multiplier = 1.0
        experience_level = employee_data.get('experience_level', '').lower()
        if experience_level == 'junior':
            if not self.is_advanced_training(training_details.get('training_name', '')):
                experience_multiplier = 1.2
        elif experience_level == 'senior':
            if self.is_advanced_training(training_details.get('training_name', '')):
                experience_multiplier = 1.2
        
        final_score = base_score * position_multiplier * division_multiplier * experience_multiplier
        return max(0.1, min(10.0, final_score))  # Ensure score is between 0.1 and 10.0
    
    def get_training_details(self, training_school: str) -> Optional[Dict]:
        """Get training details from database based on school/category"""
        try:
            # Find training that matches the school category
            matching_trainings = []
            for training_id, details in self.training_database.items():
                if training_school.lower() in details.get('school', '').lower():
                    matching_trainings.append({**details, 'training_id': training_id})
            
            # If we have matches, return the most appropriate one
            if matching_trainings:
                return matching_trainings[0]
            
            # If no exact match, try partial matching
            for training_id, details in self.training_database.items():
                # Check for partial matches in school name
                school_words = training_school.lower().split()
                if any(word in details.get('school', '').lower() for word in school_words):
                    return {**details, 'training_id': training_id}
            
            # If still no match, return a generic training template
            return {
                'training_id': f'GENERIC_{training_school.replace(" ", "_").upper()}',
                'training_name': f'Training Program for {training_school}',
                'school': training_school,
                'target_division': 'general',
                'target_level': 'ALL',
                'duration_days': 3,
                'cost': 5000000,
                'learning_objectives': ['Competency development', 'Skill enhancement'],
                'job_family': 'General'
            }
        except Exception as e:
            st.error(f"Error in get_training_details: {e}")
            return None
    
    def recommend_training(self, assessment_data: Dict) -> Dict:
        """Main function to generate training recommendations"""
        try:
            # Step 1: Identify priority areas
            priority_areas = self.identify_priority_areas(assessment_data)
            
            recommendations = []
            
            # Step 2: Generate recommendations for each priority area
            for competency, score in priority_areas:
                # Get potential trainings for this competency
                potential_trainings = self.competency_training_mapping.get(competency, [])
                
                if not potential_trainings:
                    continue
                
                # Filter based on employee context
                filtered_trainings = self.filter_by_context(
                    potential_trainings,
                    assessment_data.get('current_position', ''),
                    assessment_data.get('division', ''),
                    assessment_data.get('experience_level', '')
                )
                
                # Score and rank trainings
                for training_school in filtered_trainings:
                    training_details = self.get_training_details(training_school)
                    if not training_details:
                        continue
                    
                    relevance_score = self.calculate_relevance_score(
                        competency, score, training_details, assessment_data
                    )
                    
                    recommendation = {
                        'competency_gap': competency,
                        'current_score': score,
                        'training_details': training_details,
                        'relevance_score': relevance_score,
                        'priority_level': self.get_priority_level(score),
                        'expected_improvement': min(2.0, 5.0 - score),
                        'timeline': self._get_timeline(self.get_priority_level(score))
                    }
                    
                    recommendations.append(recommendation)
            
            # Step 3: Sort and filter top recommendations
            recommendations.sort(key=lambda x: (x['priority_level'], -x['relevance_score']))
            top_recommendations = recommendations[:3]
            
            # Step 4: Build response
            return self._build_response(assessment_data, top_recommendations)
            
        except Exception as e:
            st.error(f"Error in recommend_training: {e}")
            return {
                'error': str(e),
                'employee_id': assessment_data.get('employee_id', 'Unknown'),
                'recommendations': [],
                'summary': {'total_recommendations': 0, 'total_estimated_cost': 0, 'total_estimated_duration': 0}
            }
    
    def _get_timeline(self, priority_level: int) -> str:
        """Get timeline based on priority level"""
        timelines = {
            1: "Immediate (within 1 month)",
            2: "High Priority (within 3 months)",
            3: "Medium Priority (within 6 months)", 
            4: "Low Priority (within 12 months)"
        }
        return timelines.get(priority_level, "To be scheduled")
    
    def _build_response(self, assessment_data: Dict, recommendations: List[Dict]) -> Dict:
        """Build formatted response"""
        try:
            total_cost = sum(rec['training_details']['cost'] for rec in recommendations if rec['training_details'])
            total_duration = sum(rec['training_details']['duration_days'] for rec in recommendations if rec['training_details'])
            
            response = {
                'employee_id': assessment_data.get('employee_id', 'Unknown'),
                'assessment_date': datetime.now().strftime('%Y-%m-%d'),
                'recommendations': [],
                'development_path': {
                    'critical': [],
                    'high_priority': [],
                    'medium_priority': []
                },
                'summary': {
                    'total_recommendations': len(recommendations),
                    'total_estimated_cost': total_cost,
                    'total_estimated_duration': total_duration
                }
            }
            
            for i, rec in enumerate(recommendations, 1):
                formatted_rec = {
                    'priority': i,
                    'competency_gap': rec['competency_gap'],
                    'current_score': rec['current_score'],
                    'target_score': min(5.0, rec['current_score'] + rec['expected_improvement']),
                    'recommended_training': rec['training_details'],
                    'relevance_score': round(rec['relevance_score'], 2),
                    'expected_improvement': rec['expected_improvement'],
                    'timeline': rec['timeline']
                }
                response['recommendations'].append(formatted_rec)
                
                # Categorize by priority
                if rec['priority_level'] == 1:
                    response['development_path']['critical'].append(rec['competency_gap'])
                elif rec['priority_level'] == 2:
                    response['development_path']['high_priority'].append(rec['competency_gap'])
                else:
                    response['development_path']['medium_priority'].append(rec['competency_gap'])
            
            return response
        except Exception as e:
            st.error(f"Error in _build_response: {e}")
            return {
                'error': str(e),
                'employee_id': assessment_data.get('employee_id', 'Unknown'),
                'recommendations': [],
                'summary': {'total_recommendations': 0, 'total_estimated_cost': 0, 'total_estimated_duration': 0}
            }


# Initialize the system
@st.cache_resource
def load_training_system():
    """Load and cache the training recommendation system"""
    return TrainingRecommendationSystem()


def create_competency_chart(scores_dict, title, competency_labels):
    """Create radar chart for competency scores"""
    categories = list(scores_dict.keys())
    values = list(scores_dict.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=[competency_labels.get(cat, cat.replace('_', ' ').title()) for cat in categories],
        fill='toself',
        name=title,
        line_color='rgb(31, 119, 180)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        showlegend=False,
        title=f"{title} Competency Radar",
        height=400
    )
    
    return fig


def create_priority_chart(priority_areas):
    """Create bar chart for priority areas"""
    competencies = [area[0].replace('_', ' ').title() for area in priority_areas]
    scores = [area[1] for area in priority_areas]
    
    # Color mapping based on score
    colors = []
    for score in scores:
        if score < 2.0:
            colors.append('#ff4444')  # Critical - Red
        elif score < 3.0:
            colors.append('#ff8800')  # High - Orange
        elif score < 3.5:
            colors.append('#2196F3')  # Medium - Blue
        else:
            colors.append('#4CAF50')  # Low - Green
    
    fig = go.Figure(data=[
        go.Bar(
            x=competencies,
            y=scores,
            marker_color=colors,
            text=[f"{score:.1f}" for score in scores],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title="Top 5 Priority Areas (Lowest Scores)",
        xaxis_title="Competencies",
        yaxis_title="Current Score",
        yaxis=dict(range=[0, 5]),
        height=400
    )
    
    return fig


def display_training_card(rec, index):
    """Display a training recommendation card"""
    training = rec['recommended_training']
    
    # Priority badge
    priority_level = None
    if rec['current_score'] < 2.0:
        priority_class = "priority-critical"
        priority_level = "CRITICAL"
    elif rec['current_score'] < 3.0:
        priority_class = "priority-high" 
        priority_level = "HIGH"
    else:
        priority_class = "priority-medium"
        priority_level = "MEDIUM"
    
    st.markdown(f"""
    <div class="training-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h4 style="margin: 0;">{index}. {training['training_name']}</h4>
            <span class="{priority_class}">{priority_level}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.write(f"**🏫 School:** {training['school']}")
        st.write(f"**📊 Current Score:** {rec['current_score']:.1f}/5 → **🎯 Target:** {rec['target_score']:.1f}/5")
        st.write(f"**🔧 Gap:** {rec['competency_gap'].replace('_', ' ').title()}")
        st.write(f"**⏰ Timeline:** {rec['timeline']}")
    
    with col2:
        st.metric("Duration", f"{training['duration_days']} days")
        st.metric("Relevance", f"{rec['relevance_score']:.1f}/10")
    
    with col3:
        st.metric("Investment", f"Rp {training['cost']:,}")
        st.metric("Improvement", f"+{rec['expected_improvement']:.1f}")
    
    with st.expander(f"📚 Learning Objectives - {training['training_name']}", expanded=False):
        for i, objective in enumerate(training.get('learning_objectives', []), 1):
            st.write(f"{i}. {objective}")
    
    st.markdown("---")


def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🎯 Training Recommendation System</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem; color: #666;">
        <p>Sistem Rekomendasi Pelatihan Berbasis Machine Learning untuk Pengembangan Kompetensi Karyawan</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize system
    trs = load_training_system()
    
    # Initialize session state
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = None
    if 'assessment_data' not in st.session_state:
        st.session_state.assessment_data = None
    
    # Sidebar for input
    with st.sidebar:
        st.header("📋 Employee Information")
        
        # Basic Information
        employee_id = st.text_input("Employee ID", value="EMP001")
        position = st.selectbox("Position", trs.positions, index=4)
        division = st.selectbox("Division", [d.title() for d in trs.divisions], index=0)
        experience = st.selectbox("Experience Level", ["Junior (0-3 years)", "Mid Level (3-7 years)", "Senior (7+ years)"], index=2)
        
        st.markdown("---")
        
        # Sample data buttons
        st.subheader("📊 Quick Test")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🌱 Plantation Manager"):
                st.session_state.sample_data = "plantation_manager"
        
        with col2:
            if st.button("💰 Finance Staff"):
                st.session_state.sample_data = "finance_staff"
        
        if st.button("💻 IT Supervisor"):
            st.session_state.sample_data = "it_supervisor"
    
    # Main content area
    main_tabs = st.tabs(["📝 Assessment Input", "📊 Results & Analytics", "🎯 Recommendations", "📈 System Overview"])
    
    with main_tabs[0]:
        st.header("🎯 Competency Assessment")
        
        # Handle sample data loading
        default_scores = {}
        if hasattr(st.session_state, 'sample_data') and st.session_state.sample_data:
            sample_cases = {
                'plantation_manager': {
                    'core': {'information_seeking': 1.5, 'resilience': 3.2, 'achievement_orientation': 2.1, 'concern_for_order': 3.8, 'organizational_commitment': 2.8, 'ethical_oriented': 3.5},
                    'managerial': {'building_collaborative_relationship': 2.5, 'business_savvy': 1.8, 'customer_focus': 3.1, 'strategic_orientation': 2.0, 'sustainability_mindset': 3.4, 'execution_focused': 3.0, 'digital_literate': 1.9},
                    'leadership': {'creativity_innovation': 2.3, 'transformational_leadership': 2.7, 'nurturing_empowering_people': 3.1, 'managing_equality_diversity': 2.9}
                },
                'finance_staff': {
                    'core': {'information_seeking': 2.8, 'resilience': 2.1, 'achievement_orientation': 1.9, 'concern_for_order': 1.5, 'organizational_commitment': 3.2, 'ethical_oriented': 1.8},
                    'managerial': {'building_collaborative_relationship': 3.0, 'business_savvy': 1.7, 'customer_focus': 2.9, 'strategic_orientation': 2.5, 'sustainability_mindset': 3.1, 'execution_focused': 2.8, 'digital_literate': 2.2},
                    'leadership': {'creativity_innovation': 2.6, 'transformational_leadership': 3.0, 'nurturing_empowering_people': 2.8, 'managing_equality_diversity': 3.1}
                },
                'it_supervisor': {
                    'core': {'information_seeking': 4.2, 'resilience': 3.5, 'achievement_orientation': 1.8, 'concern_for_order': 3.0, 'organizational_commitment': 2.1, 'ethical_oriented': 3.8},
                    'managerial': {'building_collaborative_relationship': 1.9, 'business_savvy': 2.8, 'customer_focus': 3.2, 'strategic_orientation': 1.6, 'sustainability_mindset': 3.0, 'execution_focused': 3.4, 'digital_literate': 4.1},
                    'leadership': {'creativity_innovation': 1.7, 'transformational_leadership': 2.2, 'nurturing_empowering_people': 1.5, 'managing_equality_diversity': 2.8}
                }
            }
            
            if st.session_state.sample_data in sample_cases:
                default_scores = sample_cases[st.session_state.sample_data]
                st.success(f"✅ Loaded sample data for {st.session_state.sample_data.replace('_', ' ').title()}")
                # Clear the sample_data flag to prevent reloading
                st.session_state.sample_data = None
        
        # Assessment input sections
        assessment_tabs = st.tabs(["🎯 Core Competencies", "👔 Managerial Competencies", "👑 Leadership Competencies"])
        
        with assessment_tabs[0]:
            st.subheader("🎯 Core Competencies (Scale 1-5)")
            core_cols = st.columns(2)
            
            core_competency_scores = {}
            core_competencies = ['information_seeking', 'resilience', 'achievement_orientation', 'concern_for_order', 'organizational_commitment', 'ethical_oriented']
            
            for i, comp in enumerate(core_competencies):
                col = core_cols[i % 2]
                with col:
                    default_val = default_scores.get('core', {}).get(comp, 3.0)
                    score = st.slider(
                        trs.competency_labels[comp],
                        min_value=1.0,
                        max_value=5.0,
                        value=float(default_val),
                        step=0.1,
                        key=f"core_{comp}"
                    )
                    core_competency_scores[comp] = score
        
        with assessment_tabs[1]:
            st.subheader("👔 Managerial Competencies (Scale 1-5)")
            mgr_cols = st.columns(2)
            
            managerial_competency_scores = {}
            managerial_competencies = ['building_collaborative_relationship', 'business_savvy', 'customer_focus', 'strategic_orientation', 'sustainability_mindset', 'execution_focused', 'digital_literate']
            
            for i, comp in enumerate(managerial_competencies):
                col = mgr_cols[i % 2]
                with col:
                    default_val = default_scores.get('managerial', {}).get(comp, 3.0)
                    score = st.slider(
                        trs.competency_labels[comp],
                        min_value=1.0,
                        max_value=5.0,
                        value=float(default_val),
                        step=0.1,
                        key=f"mgr_{comp}"
                    )
                    managerial_competency_scores[comp] = score
        
        with assessment_tabs[2]:
            st.subheader("👑 Leadership Competencies (Scale 1-5)")
            lead_cols = st.columns(2)
            
            leadership_competency_scores = {}
            leadership_competencies = ['creativity_innovation', 'transformational_leadership', 'nurturing_empowering_people', 'managing_equality_diversity']
            
            for i, comp in enumerate(leadership_competencies):
                col = lead_cols[i % 2]
                with col:
                    default_val = default_scores.get('leadership', {}).get(comp, 3.0)
                    score = st.slider(
                        trs.competency_labels[comp],
                        min_value=1.0,
                        max_value=5.0,
                        value=float(default_val),
                        step=0.1,
                        key=f"lead_{comp}"
                    )
                    leadership_competency_scores[comp] = score
        
        # Generate recommendations button
        if st.button("🚀 Generate Training Recommendations", type="primary", use_container_width=True):
            # Prepare assessment data
            assessment_data = {
                'employee_id': employee_id,
                'current_position': position,
                'division': division.lower(),
                'experience_level': experience.split()[0].lower(),
                'core_competency_scores': core_competency_scores,
                'managerial_competency_scores': managerial_competency_scores,
                'leadership_competency_scores': leadership_competency_scores
            }
            
            # Generate recommendations
            with st.spinner("🤖 Analyzing competency gaps and generating personalized recommendations..."):
                recommendations = trs.recommend_training(assessment_data)
                st.session_state.recommendations = recommendations
                st.session_state.assessment_data = assessment_data
            
            st.success("✅ Recommendations generated successfully!")
    
    # with main_tabs[1]:
    #     st.header("📊 Results & Analytics")
        
    #     if hasattr(st.session_state, 'recommendations') and hasattr(st.session_state, 'assessment_data'):
    #         if st.session_state.recommendations and st.session_state.assessment_data:
    #             rec_data = st.session_state.recommendations
    #             assess_data = st.session_state.assessment_data
            
    #         # Summary metrics
    #         st.subheader("📈 Summary Metrics")
    #         metric_cols = st.columns(4)
            
    #         with metric_cols[0]:
    #             st.metric(
    #                 "🎯 Total Recommendations",
    #                 rec_data['summary']['total_recommendations']
    #             )
            
    #         with metric_cols[1]:
    #             st.metric(
    #                 "💰 Total Investment",
    #                 f"Rp {rec_data['summary']['total_estimated_cost']:,}"
    #             )
            
    #         with metric_cols[2]:
    #             st.metric(
    #                 "⏱️ Total Duration",
    #                 f"{rec_data['summary']['total_estimated_duration']} days"
    #             )
            
    #         with metric_cols[3]:
    #             critical_count = len(rec_data['development_path']['critical'])
    #             st.metric(
    #                 "🚨 Critical Areas",
    #                 critical_count,
    #                 delta=f"-{critical_count} gaps to address"
    #             )
            
    #         st.markdown("---")
            
    #         # Charts
    #         chart_cols = st.columns(2)
            
    #         with chart_cols[0]:
    #             # Competency radar charts
    #             core_chart = create_competency_chart(assess_data['core_competency_scores'], "Core", trs.competency_labels)
    #             st.plotly_chart(core_chart, use_container_width=True)
                
    #             managerial_chart = create_competency_chart(assess_data['managerial_competency_scores'], "Managerial", trs.competency_labels)
    #             st.plotly_chart(managerial_chart, use_container_width=True)
            
    #         with chart_cols[1]:
    #             leadership_chart = create_competency_chart(assess_data['leadership_competency_scores'], "Leadership", trs.competency_labels)
    #             st.plotly_chart(leadership_chart, use_container_width=True)
                
    #             # Priority areas chart
    #             priority_areas = trs.identify_priority_areas(assess_data)
    #             priority_chart = create_priority_chart(priority_areas)
    #             st.plotly_chart(priority_chart, use_container_width=True)
            
    #     else:
    #         st.info("📝 Please complete the assessment first to see analytics.")
    # Perbaikan untuk bagian Results & Analytics (ganti baris 1024-1047)
    
    with main_tabs[1]:
        st.header("📊 Results & Analytics")
        
        # Perbaikan: Pengecekan yang tepat untuk session state
        if (st.session_state.recommendations is not None and 
            st.session_state.assessment_data is not None):
            
            rec_data = st.session_state.recommendations
            assess_data = st.session_state.assessment_data
            
            # Summary metrics
            st.subheader("📈 Summary Metrics")
            metric_cols = st.columns(4)
            
            with metric_cols[0]:
                st.metric(
                    "🎯 Total Recommendations",
                    rec_data['summary']['total_recommendations']
                )
            
            with metric_cols[1]:
                st.metric(
                    "💰 Total Investment",
                    f"Rp {rec_data['summary']['total_estimated_cost']:,}"
                )
            
            with metric_cols[2]:
                st.metric(
                    "⏱️ Total Duration",
                    f"{rec_data['summary']['total_estimated_duration']} days"
                )
            
            with metric_cols[3]:
                critical_count = len(rec_data['development_path']['critical'])
                st.metric(
                    "🚨 Critical Areas",
                    critical_count,
                    delta=f"-{critical_count} gaps to address"
                )
            
            st.markdown("---")
            
            # Charts
            chart_cols = st.columns(2)
            
            with chart_cols[0]:
                # Competency radar charts
                core_chart = create_competency_chart(assess_data['core_competency_scores'], "Core", trs.competency_labels)
                st.plotly_chart(core_chart, use_container_width=True)
                
                managerial_chart = create_competency_chart(assess_data['managerial_competency_scores'], "Managerial", trs.competency_labels)
                st.plotly_chart(managerial_chart, use_container_width=True)
            
            with chart_cols[1]:
                leadership_chart = create_competency_chart(assess_data['leadership_competency_scores'], "Leadership", trs.competency_labels)
                st.plotly_chart(leadership_chart, use_container_width=True)
                
                # Priority areas chart
                priority_areas = trs.identify_priority_areas(assess_data)
                priority_chart = create_priority_chart(priority_areas)
                st.plotly_chart(priority_chart, use_container_width=True)
            
        else:
            st.info("📝 Please complete the assessment first to see analytics.")
        
        
    
    with main_tabs[2]:
        st.header("🎯 Training Recommendations")
        
        if st.session_state.recommendations:
            rec_data = st.session_state.recommendations
            
            if rec_data.get('recommendations'):
                st.subheader("📚 Personalized Training Recommendations")
                
                for i, rec in enumerate(rec_data['recommendations'], 1):
                    display_training_card(rec, i)
                
                # Development path
                st.subheader("🛤️ Development Path")
                path_cols = st.columns(3)
                
                with path_cols[0]:
                    st.error("🚨 **Critical Priority**")
                    for gap in rec_data.get('development_path', {}).get('critical', []):
                        st.write(f"• {gap.replace('_', ' ').title()}")
                
                with path_cols[1]:
                    st.warning("⚠️ **High Priority**")
                    for gap in rec_data.get('development_path', {}).get('high_priority', []):
                        st.write(f"• {gap.replace('_', ' ').title()}")
                
                with path_cols[2]:
                    st.info("📋 **Medium Priority**")
                    for gap in rec_data.get('development_path', {}).get('medium_priority', []):
                        st.write(f"• {gap.replace('_', ' ').title()}")
                
                # Export options
                st.markdown("---")
                st.subheader("📤 Export Options")
                
                export_cols = st.columns(3)
                
                with export_cols[0]:
                    if st.button("📊 Export to JSON"):
                        st.download_button(
                            label="Download JSON",
                            data=json.dumps(rec_data, indent=2, ensure_ascii=False),
                            file_name=f"training_recommendations_{rec_data.get('employee_id', 'unknown')}.json",
                            mime="application/json"
                        )
                
                with export_cols[1]:
                    if st.button("📋 Generate Report"):
                        # Create a simple report
                        report = f"""
# Training Recommendation Report

**Employee ID:** {rec_data.get('employee_id', 'Unknown')}
**Assessment Date:** {rec_data.get('assessment_date', 'Unknown')}
**Total Investment:** Rp {rec_data.get('summary', {}).get('total_estimated_cost', 0):,}
**Total Duration:** {rec_data.get('summary', {}).get('total_estimated_duration', 0)} days

## Recommendations:

"""
                        for i, rec in enumerate(rec_data.get('recommendations', []), 1):
                            training = rec.get('recommended_training', {})
                            report += f"""
### {i}. {training.get('training_name', 'Unknown Training')}
- **School:** {training.get('school', 'Unknown')}
- **Current Score:** {rec.get('current_score', 0)}/5 → **Target:** {rec.get('target_score', 0)}/5
- **Duration:** {training.get('duration_days', 0)} days
- **Cost:** Rp {training.get('cost', 0):,}
- **Timeline:** {rec.get('timeline', 'Unknown')}

"""
                        
                        st.download_button(
                            label="Download Report",
                            data=report,
                            file_name=f"training_report_{rec_data.get('employee_id', 'unknown')}.md",
                            mime="text/markdown"
                        )
                
                with export_cols[2]:
                    if st.button("📧 Email Summary"):
                        st.info("Email functionality would be implemented here")
            
            else:
                st.warning("⚠️ No recommendations found. Please check the assessment data.")
        
        else:
            st.info("📝 Please complete the assessment first to get recommendations.")
    
    with main_tabs[3]:
        st.header("📈 System Overview")
        
        # System statistics
        st.subheader("🏢 Training Database Coverage")
        
        stats_cols = st.columns(4)
        
        with stats_cols[0]:
            st.metric("📚 Total Training Programs", len(trs.training_database))
        
        with stats_cols[1]:
            divisions_covered = set(training['target_division'] for training in trs.training_database.values())
            st.metric("🏢 Divisions Covered", len(divisions_covered))
        
        with stats_cols[2]:
            total_competencies = len(trs.competency_training_mapping)
            st.metric("🎯 Competencies Mapped", total_competencies)
        
        with stats_cols[3]:
            avg_cost = sum(training['cost'] for training in trs.training_database.values()) / len(trs.training_database)
            st.metric("💰 Average Training Cost", f"Rp {avg_cost:,.0f}")
        
        st.markdown("---")
        
        # Training database overview
        st.subheader("📊 Training Programs by Division")
        
        # Create division distribution chart
        division_counts = {}
        for training in trs.training_database.values():
            div = training['target_division'].title()
            division_counts[div] = division_counts.get(div, 0) + 1
        
        fig = px.pie(
            values=list(division_counts.values()),
            names=list(division_counts.keys()),
            title="Training Programs Distribution by Division"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Training costs distribution
        st.subheader("💰 Training Costs Distribution")
        
        costs = [training['cost'] for training in trs.training_database.values()]
        names = [training['training_name'][:50] + "..." if len(training['training_name']) > 50 
                else training['training_name'] for training in trs.training_database.values()]
        
        fig = px.bar(
            x=names,
            y=costs,
            title="Training Costs by Program",
            labels={'x': 'Training Program', 'y': 'Cost (Rp)'}
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Algorithm explanation
        st.subheader("🤖 How the Algorithm Works")
        
        with st.expander("📖 Algorithm Details", expanded=False):
            st.markdown("""
            ### 🔍 **Step 1: Gap Analysis**
            - Analyzes all competency scores (Core, Managerial, Leadership)
            - Identifies top 5 priority areas with lowest scores
            - Categorizes gaps as Critical (<2.0), High (2.0-3.0), or Medium (3.0-3.5)

            ### 🎯 **Step 2: Training Mapping**
            - Maps each competency gap to relevant training programs
            - Uses predefined competency-to-training matrix
            - Considers 18+ training programs across 11 divisions

            ### 🔧 **Step 3: Context Filtering**
            - Filters based on employee position (Staff/Manager/Executive)
            - Matches training to employee division and experience level
            - Applies business rules for training appropriateness

            ### 📊 **Step 4: Relevance Scoring**
            - Calculates base relevance score: 5.0 - current_score
            - Applies contextual multipliers:
              - Position Match: 1.5x for management trainings
              - Division Match: 1.3x for division-specific programs  
              - Experience Match: 1.2x for level-appropriate training

            ### 🎯 **Step 5: Recommendation Ranking**
            - Sorts by priority level (Critical > High > Medium)
            - Ranks by relevance score within each priority
            - Returns top 3 most relevant recommendations
            """)
        
        # Sample data showcase
        st.subheader("🧪 Sample Test Cases")
        
        sample_cols = st.columns(3)
        
        with sample_cols[0]:
            if st.button("🌱 Test Plantation Manager", key="test1"):
                st.session_state.sample_data = "plantation_manager"
                st.rerun()
        
        with sample_cols[1]:
            if st.button("💰 Test Finance Staff", key="test2"):
                st.session_state.sample_data = "finance_staff"
                st.rerun()
        
        with sample_cols[2]:
            if st.button("💻 Test IT Supervisor", key="test3"):
                st.session_state.sample_data = "it_supervisor"
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>🎯 <strong>Training Recommendation System</strong> | Powered by Machine Learning | Built with Streamlit</p>
        <p>📧 For support or feature requests, contact your HR Analytics team</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
