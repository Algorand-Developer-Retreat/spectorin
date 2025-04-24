# core/ai_agents/ollama_agent.py
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import List, Dict, Any
import logging
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from .llm_providers import LLMProvider

logger = logging.getLogger(__name__)

class OllamaAgent:
    def __init__(self, memory_efficient: bool = False):
        self.memory_efficient = memory_efficient
        if not memory_efficient:
            self.llm_provider = LLMProvider()
            provider_info = self.llm_provider.get_available_provider()
            if provider_info:
                self.provider_name, self.llm = provider_info
                self.llm_available = True
                logger.info(f"Using {self.provider_name} as LLM provider")
            else:
                self.llm_available = False
                logger.warning("No LLM providers available")
        else:
            self.llm_available = False
            logger.info("Running in memory-efficient mode (no LLM analysis)")

    def _chunk_code(self, code: str, chunk_size: int = 1000) -> List[str]:
        """Split code into smaller chunks"""
        lines = code.split('\n')
        chunks = []
        current_chunk = []
        current_size = 0
        
        for line in lines:
            line_size = len(line)
            if current_size + line_size > chunk_size:
                chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
                current_size = line_size
            else:
                current_chunk.append(line)
                current_size += line_size
                
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
            
        return chunks

    def _process_chunk(self, chunk: str, language: str) -> List[str]:
        """Process a single code chunk"""
        try:
            prompt = PromptTemplate.from_template(
                """You are a code security expert using Phi-3 Mini. Analyze this code chunk for security vulnerabilities and best practices.

                Code:
                {code}
                
                Language: {language}
                
                Please provide a detailed analysis following these steps:
                1. Identify potential security vulnerabilities
                2. Check for common coding anti-patterns
                3. Suggest specific improvements
                4. Reference relevant security best practices
                
                Format your response as a clear, structured analysis with specific recommendations."""
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt)
            result = self._run_with_timeout(
                chain.invoke,
                {"code": chunk, "language": language},
                timeout=30  # Increased timeout for more thorough analysis
            )
            
            if result is None:
                return []
                
            return [rec.strip() for rec in result['text'].split('\n') if rec.strip()]
            
        except Exception as e:
            logger.error(f"Error processing chunk: {str(e)}")
            return []

    def generate_recommendations(self, code: str, language: str, issues: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on code analysis results"""
        if not issues:
            return ["No issues found. The contract appears to follow best practices."]
            
        if self.memory_efficient or not self.llm_available:
            logger.info("Using memory-efficient recommendations")
            return self._get_fallback_recommendations(issues)
            
        try:
            # Split code into chunks
            chunks = self._chunk_code(code)
            all_recommendations = []
            
            # Process each chunk
            for chunk in chunks:
                chunk_recommendations = self._process_chunk(chunk, language)
                all_recommendations.extend(chunk_recommendations)
            
            # If no recommendations from chunks, use fallback
            if not all_recommendations:
                logger.warning("No recommendations from chunks, using fallback")
                return self._get_fallback_recommendations(issues)
            
            # Remove duplicates and sort by priority
            unique_recommendations = list(set(all_recommendations))
            return self._prioritize_recommendations(unique_recommendations)
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return self._get_fallback_recommendations(issues)

    def _prioritize_recommendations(self, recommendations: List[str]) -> List[str]:
        """Prioritize recommendations based on keywords"""
        high_priority = []
        medium_priority = []
        low_priority = []
        
        high_keywords = ['security', 'vulnerability', 'critical', 'validation', 'access control']
        medium_keywords = ['optimization', 'performance', 'documentation', 'testing']
        
        for rec in recommendations:
            rec_lower = rec.lower()
            if any(keyword in rec_lower for keyword in high_keywords):
                high_priority.append(rec)
            elif any(keyword in rec_lower for keyword in medium_keywords):
                medium_priority.append(rec)
            else:
                low_priority.append(rec)
                
        return high_priority + medium_priority + low_priority

    def _run_with_timeout(self, func, *args, timeout=15):
        """Run a function with a timeout"""
        with ThreadPoolExecutor() as executor:
            future = executor.submit(func, *args)
            try:
                return future.result(timeout=timeout)
            except TimeoutError:
                logger.warning(f"Operation timed out after {timeout} seconds")
                return None
            except Exception as e:
                logger.error(f"Error in operation: {str(e)}")
                return None

    def _get_fallback_recommendations(self, issues: List[Dict[str, Any]]) -> List[str]:
        """Generate fallback recommendations based on issue types"""
        recommendations = []
        
        # Map issue types to standard recommendations
        issue_recommendations = {
            'input-validation': [
                'Validate all external inputs using PyTeal assertion functions',
                'Implement proper bounds checking for numeric inputs',
                'Validate array indices before access'
            ],
            'state-management': [
                'Implement proper state initialization checks',
                'Use local state for contract-specific data',
                'Implement proper state cleanup in clear state program'
            ],
            'error-handling': [
                'Implement proper error handling for all operations',
                'Use Try-Catch blocks for critical operations',
                'Add proper error messages for debugging'
            ],
            'access-control': [
                'Implement proper access control mechanisms',
                'Add creator checks for sensitive operations',
                'Use proper authorization checks'
            ],
            'gas-optimization': [
                'Optimize state access patterns',
                'Cache frequently accessed state values',
                'Minimize storage operations in loops'
            ],
            'atomic': [
                'Use atomic transfers for multiple operations',
                'Implement proper group transaction validation',
                'Add proper group size checks'
            ]
        }
        
        # Add recommendations based on issue types
        seen_types = set()
        for issue in issues:
            issue_type = issue.get('type', '').lower()
            if issue_type in issue_recommendations and issue_type not in seen_types:
                recommendations.extend(issue_recommendations[issue_type])
                seen_types.add(issue_type)
        
        # Add general recommendations
        general_recommendations = [
            'Follow PyTeal best practices',
            'Implement proper error handling',
            'Add comprehensive documentation',
            'Write unit tests for all operations',
            'Implement proper logging for debugging'
        ]
        
        recommendations.extend(general_recommendations)
        return list(set(recommendations))  # Remove duplicates

    def generate_tests(self, code: str):
        if self.memory_efficient or not self.llm_available:
            return "Test generation is not available in memory-efficient mode."
            
        try:
            # Split code into chunks
            chunks = self._chunk_code(code)
            all_tests = []
            
            # Process each chunk
            for chunk in chunks:
                prompt = PromptTemplate.from_template(
                    "Write hypothesis-style tests for the following code:\n\n{code}"
                )
                chain = LLMChain(llm=self.llm, prompt=prompt)
                
                result = self._run_with_timeout(
                    chain.invoke,
                    {"code": chunk},
                    timeout=15
                )
                
                if result is not None:
                    all_tests.append(result['text'])
            
            if not all_tests:
                return "Test generation failed. Please try again or use a smaller code sample."
                
            return "\n\n".join(all_tests)
            
        except Exception as e:
            logger.error(f"Error generating tests: {str(e)}")
            return "Failed to generate tests due to LLM service error."

    def explain(self, code: str):
        if self.memory_efficient or not self.llm_available:
            return "Vulnerability explanation is not available in memory-efficient mode."
            
        try:
            # Split code into chunks
            chunks = self._chunk_code(code)
            all_explanations = []
            
            # Process each chunk
            for chunk in chunks:
                prompt = PromptTemplate.from_template(
                    "Explain any vulnerabilities in the following code:\n\n{code}"
                )
                chain = LLMChain(llm=self.llm, prompt=prompt)
                
                result = self._run_with_timeout(
                    chain.invoke,
                    {"code": chunk},
                    timeout=15
                )
                
                if result is not None:
                    all_explanations.append(result['text'])
            
            if not all_explanations:
                return "Vulnerability explanation failed. Please try again or use a smaller code sample."
                
            return "\n\n".join(all_explanations)
            
        except Exception as e:
            logger.error(f"Error explaining vulnerabilities: {str(e)}")
            return "Failed to explain vulnerabilities due to LLM service error."
