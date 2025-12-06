"""
AI Semantic Resume Analyzer - Strict Pedagogical Mode

This module provides rigorous AI-powered evaluation with strict penalties,
detailed feedback, and rewritten bullet examples for learning.

NO UI, NO DATABASE - Pure backend processing.
"""

import os
import re
import json
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class AISemanticAnalyzer:
    """Strict AI-powered analyzer with pedagogical feedback."""
    
    def __init__(self):
        """Initialize the analyzer with Google Gemini API."""
        # Load from .env file if it exists (for local development)
        # On Render, load from secret files location
        load_dotenv()  # Try local .env first
        load_dotenv('/etc/secrets/.env')  # Then try Render secret files location
        
        # Use dedicated API key for AI analyzer, fallback to general key
        self.api_key = os.getenv("AI_GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        
        # Debug logging
        print(f"AI Analyzer - API Key found: {bool(self.api_key)}")
        print(f"AI Analyzer - Gemini available: {GEMINI_AVAILABLE}")
        
        if self.api_key and GEMINI_AVAILABLE:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel("gemini-2.5-flash")
                self.available = True
                print("✅ AI Semantic Analyzer initialized successfully")
            except Exception as e:
                print(f"❌ AI Semantic Analyzer initialization failed: {e}")
                self.available = False
        else:
            if not self.api_key:
                print("❌ AI Semantic Analyzer: No API key found")
            if not GEMINI_AVAILABLE:
                print("❌ AI Semantic Analyzer: google-generativeai not installed")
            self.available = False
    
    def analyze(self, resume_text: str) -> Dict[str, Any]:
        """
        Strict AI analysis with pedagogical feedback and rewritten examples.
        
        Args:
            resume_text: Plain text extracted from resume (OCR output)
            
        Returns:
            Dictionary with strict AI score and detailed teaching feedback
        """
        if not self.available:
            return {
                'score': 0,
                'error': 'AI analysis unavailable - missing API key or google-generativeai package',
                'strengths': [],
                'weaknesses': ['AI analysis could not be performed']
            }
        
        if not resume_text or len(resume_text.strip()) < 50:
            return {
                'score': 0,
                'strengths': [],
                'weaknesses': ['Resume text is too short for meaningful AI analysis']
            }
        
        try:
            print("=" * 60)
            print("🤖 AI SEMANTIC ANALYZER - LLM PROCESSING")
            print("=" * 60)
            
            # Create strict pedagogical prompt
            print("📝 Creating AI analysis prompt...")
            prompt = self._create_strict_prompt(resume_text)
            print(f"✓ Prompt created ({len(prompt)} characters)")
            
            # Get AI response with JSON output
            print("🔄 Sending request to Gemini API (gemini-2.5-flash)...")
            print("⏳ Waiting for AI response... (this may take 5-15 seconds)")
            
            import time
            start_time = time.time()
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json"
                )
            )
            
            elapsed_time = time.time() - start_time
            print(f"⏱️  API call completed in {elapsed_time:.2f} seconds")
            
            print("✅ AI response received successfully!")
            print(f"📊 Response size: {len(response.text)} characters")
            
            # Parse JSON response
            print("🔍 Parsing AI response JSON...")
            result = json.loads(response.text)
            print(f"✓ JSON parsed - Score: {result.get('ai_ats_score', 0)}/100")
            
            # Transform to our standard format
            print("🔄 Transforming AI output to standard format...")
            transformed = self._transform_strict_output(result)
            print("✅ AI Semantic Analysis Complete!")
            print("=" * 60)
            
            return transformed
            
        except json.JSONDecodeError as e:
            # Fallback if JSON parsing fails
            import traceback
            print(f"❌ AI Semantic Analyzer - JSON parsing failed!")
            print(f"Error: {str(e)}")
            print(traceback.format_exc())
            print("=" * 60)
            return {
                'score': 0,
                'error': f'AI response parsing failed: {str(e)}',
                'strengths': [],
                'weaknesses': ['AI analysis encountered a JSON parsing error']
            }
        except Exception as e:
            import traceback
            print(f"❌ AI Semantic Analyzer - Analysis failed!")
            print(f"Error: {str(e)}")
            print(traceback.format_exc())
            print("=" * 60)
            return {
                'score': 0,
                'error': f'AI analysis failed: {str(e)}',
                'strengths': [],
                'weaknesses': ['AI analysis encountered an error']
            }
    
    def _create_strict_prompt(self, resume_text: str) -> str:
        """Create balanced, constructive evaluation prompt."""
        return f"""SYSTEM:
You are "AI Resume Analyzer — Balanced Mode", an automated resume assessor that provides constructive, fair evaluation of OCR-extracted resume text. Your approach is balanced: recognize strengths while identifying areas for improvement. Your goals:
1. Produce a fair, balanced AI-based score (0–100) that reflects both strengths and growth areas.
2. Identify genuine issues while being understanding of student/early-career contexts.
3. Provide concrete, actionable improvements with helpful rewritten bullet examples.
4. Be encouraging and constructive — focus on helping candidates improve.
5. Output JSON exactly in the schema at the end.

RESUME TEXT:
{resume_text}

INSTRUCTIONS (apply in order):

A. PARSING ASSUMPTION
- If OCR noise exists (>10% of lines contain unreadable tokens), note it but apply only a minor penalty: subtract 5 points maximum.
- Be forgiving of minor formatting issues from PDF extraction.

B. EVIDENCE RULE (Moderate)
- For claimed skills, look for supporting evidence in Experience/Projects sections.
  - Strong evidence = explicit usage with context and results
  - Partial evidence = mentioned in project/role but without details → treat as 0.7 credit (70%)
  - No evidence but skill is relevant to role → treat as 0.5 credit (50%)
- Don't penalize students for listing foundational skills even without extensive project evidence.

C. SENIORITY VALIDATION (Lenient)
- If resume claims senior-level roles but experience seems limited, note it constructively.
- Only apply penalty (-10 points max) if there's clear mismatch (e.g., "Senior Architect" with 1 year experience).
- For students/freshers, don't penalize lack of seniority.

D. METRICS & IMPACT (Balanced)
- Recognize that not all roles have quantifiable metrics, especially for students/freshers.
- If metrics are present, give bonus points (+10 to +20).
- If missing, provide suggestions but apply minimal penalty (-5 to -10 points max).
- Value qualitative impact statements for student projects.

E. TEMPLATE / BUZZWORD DETECTION (Moderate)
- Note generic phrases but don't over-penalize (-1 point per phrase, max -5 total).
- Recognize that some standard professional language is acceptable.
- Focus on whether the overall content is substantive.

F. DEPTH & OWNERSHIP (Constructive)
- Evaluate bullets on: Action verb (1), Method/Tech (1), Outcome/Impact (2).
- If Outcome missing, reduce credit to 50% (not 25%).
- Encourage improvement rather than harsh penalties.

G. PROJECT VALIDATION (Student-Friendly)
- For freshers/students: 1-2 solid projects with clear contribution = acceptable.
- Don't hard cap scores — provide constructive feedback instead.
- Value learning projects and academic work.

H. CONTRADICTIONS & TIMELINES (Lenient)
- Only flag obvious contradictions or timeline issues.
- Minor inconsistencies → note in feedback but minimal penalty (-3 to -5 points).

I. CONSTRUCTIVE FEEDBACK (mandatory)
For improvement areas, provide:
  1. Issue label (use encouraging language)
  2. Relevant snippet from resume
  3. Severity (High/Medium/Low) — use "High" sparingly
  4. Concrete recommended fix with positive framing
  5. Two rewritten bullet examples (concise and expanded) that demonstrate best practices

J. SCORE NORMALIZATION (Balanced)
- Compute a raw AI score (0–100) by weighting:
   - Evidence & depth: 35%
   - Metrics & impact: 25%
   - Content quality: 20%
   - Seniority & role fit: 10%
   - Originality / non-template: 5%
   - Parsing cleanliness: 5%

- Start with a base score of 40 for any reasonable resume attempt.
- Add points for strengths, subtract moderately for clear issues.
- Final score should typically range 40-85 for most resumes.
- Reserve scores below 30 only for severely incomplete resumes.
- Reserve scores above 85 for truly exceptional resumes.

K. SUMMARY & LEARNING GUIDANCE
- Produce an encouraging "teaching summary" (2–4 sentences) highlighting top 2-3 actionable improvements.
- Use supportive, student-friendly language.
- Focus on "next steps" rather than deficiencies.

L. OUTPUT FORMAT (STRICT JSON)
Return only valid JSON exactly matching this schema:

{{
  "ai_ats_score": 0,
  "raw_scores": {{
    "evidence_depth": 0,
    "metrics_impact": 0,
    "seniority_fit": 0,
    "originality": 0,
    "parsing_cleanliness": 0
  }},
  "deductions_and_caps": {{
    "parsing_penalty": 0,
    "seniority_penalty": 0,
    "metrics_penalty": 0,
    "template_penalty": 0,
    "contradiction_penalty": 0,
    "further_caps": []
  }},
  "analysis_summary": {{
    "strengths": ["...", "..."],
    "weaknesses": ["...", "..."]
  }},
  "teaching_summary": "[2-4 sentence actionable, encouraging summary]",
  "issues": [
    {{
      "label": "Opportunity: Add Evidence for Skill X",
      "snippet": "relevant lines from resume_text",
      "severity": "Medium",
      "recommended_fix": "Step-by-step constructive guidance",
      "rewrites": {{
        "concise": "One-line improved example",
        "expanded": "Detailed example with tools + impact"
      }}
    }}
  ],
  "suggested_rewrites_for_role": [
    {{
      "role_or_project": "Role/Project name",
      "rewrites": [
        "Enhanced bullet 1",
        "Enhanced bullet 2"
      ]
    }}
  ]
}}"""

    def _transform_strict_output(self, strict_result: Dict[str, Any]) -> Dict[str, Any]:
        """Transform strict JSON output to standard format."""
        
        # Extract score
        score = strict_result.get('ai_ats_score', 0)
        
        # Extract strengths and weaknesses
        analysis_summary = strict_result.get('analysis_summary', {})
        strengths = analysis_summary.get('strengths', [])
        weaknesses = analysis_summary.get('weaknesses', [])
        
        # Add teaching summary to weaknesses if present
        teaching_summary = strict_result.get('teaching_summary', '')
        if teaching_summary:
            weaknesses.insert(0, f"Learning Focus: {teaching_summary}")
        
        # Build detailed insights from issues
        issues = strict_result.get('issues', [])
        detailed_insights = []
        
        for issue in issues:
            label = issue.get('label', '')
            severity = issue.get('severity', 'Medium')
            fix = issue.get('recommended_fix', '')
            rewrites = issue.get('rewrites', {})
            
            insight = f"[{severity}] {label}: {fix}"
            if rewrites:
                concise = rewrites.get('concise', '')
                if concise:
                    insight += f" | Example: {concise}"
            
            detailed_insights.append(insight)
        
        # Extract deductions for transparency
        deductions = strict_result.get('deductions_and_caps', {})
        raw_scores = strict_result.get('raw_scores', {})
        
        return {
            'score': score,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'teaching_summary': teaching_summary,
            'detailed_insights': detailed_insights,
            'raw_scores': raw_scores,
            'deductions': deductions,
            'issues': issues,
            'suggested_rewrites': strict_result.get('suggested_rewrites_for_role', []),
            # Standard fields for compatibility
            'semantic_insights': teaching_summary,
            'experience_depth': f"Evidence & Depth Score: {raw_scores.get('evidence_depth', 0)}/100",
            'impact_assessment': f"Metrics & Impact Score: {raw_scores.get('metrics_impact', 0)}/100",
            'role_level': self._determine_role_level(score, raw_scores)
        }
    
    def _determine_role_level(self, score: int, raw_scores: Dict[str, int]) -> str:
        """Determine role level based on scores."""
        seniority_fit = raw_scores.get('seniority_fit', 0)
        
        if score >= 75 and seniority_fit >= 70:
            return "Senior"
        elif score >= 55 and seniority_fit >= 50:
            return "Mid-Level"
        else:
            return "Junior"
