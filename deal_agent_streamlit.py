import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from datetime import datetime
from typing import List, Optional
import numpy as np

# Import the deal agent framework
from deal_agent_framework import DealAgentFramework
from agents.deals import Opportunity, Deal

# Page configuration
st.set_page_config(
    page_title="Deal Agent Framework Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .opportunity-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #28a745;
    }
    .deal-threshold {
        color: #dc3545;
        font-weight: bold;
    }
    .success-message {
        color: #28a745;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

class DealAgentStreamlitApp:
    def __init__(self):
        self.framework = None
        self.initialize_framework()
    
    def initialize_framework(self):
        """Initialize the deal agent framework"""
        try:
            if self.framework is None:
                with st.spinner("Initializing Deal Agent Framework..."):
                    self.framework = DealAgentFramework()
                st.success("✅ Deal Agent Framework initialized successfully!")
        except Exception as e:
            st.error(f"❌ Error initializing framework: {str(e)}")
    
    def run_agent_workflow(self):
        """Run the full agent workflow"""
        if self.framework is None:
            st.error("Framework not initialized. Please refresh the page.")
            return
        
        with st.spinner("🤖 Running agent workflow..."):
            try:
                opportunities = self.framework.run()
                if opportunities:
                    st.success(f"✅ Found {len(opportunities)} opportunities!")
                    return opportunities
                else:
                    st.info("ℹ️ No new opportunities found this run.")
                    return []
            except Exception as e:
                st.error(f"❌ Error running workflow: {str(e)}")
                return []
    
    def display_opportunities(self, opportunities: List[Opportunity]):
        """Display opportunities in a nice format"""
        if not opportunities:
            st.info("No opportunities to display.")
            return
        
        st.subheader("🎯 Current Opportunities")
        
        for i, opp in enumerate(opportunities):
            with st.expander(f"Opportunity #{i+1}: {opp.deal.product_description[:50]}...", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Deal Price", f"${opp.deal.price:.2f}")
                
                with col2:
                    st.metric("Estimated Value", f"${opp.estimate:.2f}")
                
                with col3:
                    discount_color = "normal" if opp.discount > 50 else "inverse"
                    st.metric("Discount", f"${opp.discount:.2f}", delta=f"{opp.discount:.1f}% off")
                
                st.write("**Product Description:**")
                st.write(opp.deal.product_description)
                
                st.write("**Deal URL:**")
                st.write(f"[{opp.deal.url}]({opp.deal.url})")
                
                if opp.discount > 50:
                    st.success(f"🔥 Great deal! ${opp.discount:.2f} savings!")
                elif opp.discount > 0:
                    st.info(f"💡 Good deal! ${opp.discount:.2f} savings!")
                else:
                    st.warning(f"⚠️ Deal may not be worth it. Overpriced by ${abs(opp.discount):.2f}")
    
    def display_memory_stats(self):
        """Display memory statistics"""
        if self.framework is None:
            return
        
        memory = self.framework.memory
        st.subheader("📊 Memory Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Opportunities", len(memory))
        
        with col2:
            if memory:
                avg_discount = sum(opp.discount for opp in memory) / len(memory)
                st.metric("Average Discount", f"${avg_discount:.2f}")
            else:
                st.metric("Average Discount", "$0.00")
        
        with col3:
            if memory:
                max_discount = max(opp.discount for opp in memory)
                st.metric("Best Discount", f"${max_discount:.2f}")
            else:
                st.metric("Best Discount", "$0.00")
        
        with col4:
            if memory:
                total_savings = sum(opp.discount for opp in memory)
                st.metric("Total Savings", f"${total_savings:.2f}")
            else:
                st.metric("Total Savings", "$0.00")
    
    def create_product_embedding_visualization(self):
        """Create t-SNE visualization of product embeddings"""
        try:
            with st.spinner("Creating product embedding visualization..."):
                documents, vectors, colors = self.framework.get_plot_data(max_datapoints=1000)
                
                # Check if we have enough data for t-SNE
                if len(vectors) == 0:
                    st.info("No product embeddings available for visualization.")
                    return
                
                if len(vectors) < 4:
                    st.warning(f"Not enough data for t-SNE visualization. Need at least 4 samples, but only have {len(vectors)}. Please run the agent workflow to populate the database first.")
                    return
                
                # Ensure we have enough samples for t-SNE perplexity
                min_samples = max(4, 30)  # t-SNE needs at least 4 samples, perplexity should be less than n_samples
                if len(vectors) < min_samples:
                    st.warning(f"Not enough samples for optimal t-SNE visualization. Have {len(vectors)} samples, but recommend at least {min_samples} for best results.")
                
                # Create 3D scatter plot
                fig = go.Figure(data=go.Scatter3d(
                    x=vectors[:, 0],
                    y=vectors[:, 1],
                    z=vectors[:, 2],
                    mode='markers',
                    marker=dict(
                        size=3,
                        color=colors,
                        opacity=0.6
                    ),
                    text=documents[:len(vectors)],
                    hovertemplate='<b>%{text}</b><br>' +
                                'X: %{x:.2f}<br>' +
                                'Y: %{y:.2f}<br>' +
                                'Z: %{z:.2f}<extra></extra>'
                ))
                
                fig.update_layout(
                    title=f"Product Embeddings (t-SNE 3D) - {len(vectors)} products",
                    scene=dict(
                        xaxis_title='Dimension 1',
                        yaxis_title='Dimension 2',
                        zaxis_title='Dimension 3'
                    ),
                    width=800,
                    height=600
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Show category distribution
                st.subheader("📈 Product Category Distribution")
                category_counts = {}
                for color in colors:
                    category_counts[color] = category_counts.get(color, 0) + 1
                
                if category_counts:
                    fig_pie = px.pie(
                        values=list(category_counts.values()),
                        names=list(category_counts.keys()),
                        title="Product Categories"
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("No category data available for pie chart.")
                
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
            st.info("💡 Tip: Try running the agent workflow first to populate the product database with embeddings.")
    
    def clear_memory(self):
        """Clear the memory file"""
        try:
            if os.path.exists(self.framework.MEMORY_FILENAME):
                os.remove(self.framework.MEMORY_FILENAME)
                self.framework.memory = []
                st.success("✅ Memory cleared successfully!")
            else:
                st.info("Memory file doesn't exist.")
        except Exception as e:
            st.error(f"❌ Error clearing memory: {str(e)}")
    
    def export_opportunities(self):
        """Export opportunities to CSV"""
        if not self.framework or not self.framework.memory:
            st.warning("No opportunities to export.")
            return
        
        data = []
        for opp in self.framework.memory:
            data.append({
                'Product Description': opp.deal.product_description,
                'Deal Price': opp.deal.price,
                'Estimated Value': opp.estimate,
                'Discount': opp.discount,
                'URL': opp.deal.url
            })
        
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="📥 Download Opportunities as CSV",
            data=csv,
            file_name=f"opportunities_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def main():
    # Header
    st.markdown('<h1 class="main-header">💰 Deal Agent Framework Dashboard</h1>', unsafe_allow_html=True)
    
    # Initialize the app
    app = DealAgentStreamlitApp()
    
    # Sidebar controls
    st.sidebar.header("🎛️ Controls")
    
    if st.sidebar.button("🚀 Run Agent Workflow", type="primary"):
        opportunities = app.run_agent_workflow()
        st.session_state.latest_opportunities = opportunities
    
    st.sidebar.divider()
    
    if st.sidebar.button("🗑️ Clear Memory"):
        app.clear_memory()
        st.rerun()
    
    if st.sidebar.button("📥 Export Opportunities"):
        app.export_opportunities()
    
    st.sidebar.divider()
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🎯 Opportunities", "🔍 Product Visualization"])
    
    with tab1:
        st.header("Dashboard Overview")
        
        # Display memory stats
        app.display_memory_stats()
        
        # Quick stats
        if app.framework and app.framework.memory:
            st.subheader("📈 Quick Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                good_deals = len([opp for opp in app.framework.memory if opp.discount > 50])
                st.metric("Deals Above Threshold", good_deals)
            
            with col2:
                if app.framework.memory:
                    recent_discount = app.framework.memory[-1].discount
                    st.metric("Latest Discount", f"${recent_discount:.2f}")
    
    with tab2:
        st.header("Current Opportunities")
        
        if app.framework:
            app.display_opportunities(app.framework.memory)
        else:
            st.error("Framework not initialized.")
    
    with tab3:
        st.header("Product Embedding Visualization")
        app.create_product_embedding_visualization()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            Deal Agent Framework Dashboard | Built with Streamlit
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
