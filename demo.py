#!/usr/bin/env python3
"""
Demo script for the AI Research Agent
"""
import asyncio
import json
from datetime import datetime
from agent import AIResearchAgent

async def run_demo():
    """Run a demonstration of the AI Research Agent"""
    print("🔍 AI Research Agent Demo")
    print("=" * 50)
    
    # Initialize the agent
    agent = AIResearchAgent()
    
    # Demo topics
    demo_topics = [
        "Artificial Intelligence in Healthcare",
        "Blockchain Technology Trends",
        "Quantum Computing Applications"
    ]
    
    print(f"Running demo with {len(demo_topics)} topics...")
    print()
    
    for i, topic in enumerate(demo_topics, 1):
        print(f"📋 Demo {i}/{len(demo_topics)}: {topic}")
        print("-" * 40)
        
        try:
            # Start research
            start_time = datetime.now()
            result = await agent.research_topic(topic)
            end_time = datetime.now()
            
            duration = (end_time - start_time).total_seconds()
            
            print(f"✅ Research completed in {duration:.2f} seconds")
            print(f"📊 Status: {result.status}")
            print(f"🔗 Research ID: {result.research_id}")
            print(f"📝 Steps completed: {len(result.steps)}")
            print(f"📋 Trace entries: {len(result.trace_log)}")
            
            # Show final result if available
            if result.final_result and "analysis" in result.final_result:
                analysis = result.final_result["analysis"]
                print(f"📈 Confidence Score: {analysis.get('confidence_score', 0):.2f}")
                print(f"🔍 Sources analyzed: {len(analysis.get('sources', []))}")
                print(f"💡 Key findings: {len(analysis.get('key_findings', []))}")
            
            print()
            
        except Exception as e:
            print(f"❌ Error researching '{topic}': {e}")
            print()
    
    print("🎉 Demo completed!")
    print("\nTo explore the results:")
    print("1. Start the web server: python run.py")
    print("2. Open http://localhost:8000 in your browser")
    print("3. View the research results in the web interface")

def show_agent_capabilities():
    """Show what the agent can do"""
    print("🤖 AI Research Agent Capabilities")
    print("=" * 50)
    print()
    print("📋 PLANNING:")
    print("  • Analyzes research topics intelligently")
    print("  • Generates research questions and strategies")
    print("  • Plans multi-step research workflows")
    print()
    print("🔍 EXECUTION:")
    print("  • Performs web searches with multiple queries")
    print("  • Processes and scores search results")
    print("  • Extracts relevant information from sources")
    print()
    print("🧠 ANALYSIS:")
    print("  • Synthesizes information from multiple sources")
    print("  • Identifies key findings and trends")
    print("  • Generates comprehensive summaries")
    print("  • Calculates confidence scores")
    print()
    print("✅ VALIDATION:")
    print("  • Validates result completeness and quality")
    print("  • Ensures research standards are met")
    print("  • Provides quality metrics")
    print()
    print("📊 PERSISTENCE:")
    print("  • Stores all research data in SQLite database")
    print("  • Maintains complete audit trail")
    print("  • Enables research history retrieval")
    print()
    print("🔍 EXPLAINABILITY:")
    print("  • Complete trace logs of all decisions")
    print("  • Step-by-step execution tracking")
    print("  • Transparent reasoning process")
    print("  • Debug information and metrics")
    print()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--capabilities":
        show_agent_capabilities()
    else:
        asyncio.run(run_demo())
