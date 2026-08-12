import os
import folium
from folium.plugins import HeatMap, MarkerCluster
import pandas as pd


def generate_geo_hotspots(
    file_path="data/processed/cleaned_complaints.csv",
    output_dir="reports",
):
    """Generates interactive Leaflet/Folium map HTML files for complaint density

    and SLA breach hotspots.
    """
    if not os.path.exists(file_path):
        print(
            f"❌ Processed file missing at {file_path}. Run Milestone 4 first!"
        )
        return

    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(file_path)

    print("🗺️ Generating Geographic Intelligence & Hotspot Analysis...")

    # Filter records with valid latitude and longitude
    geo_df = df[df["latitude"].notnull() & df["longitude"].notnull()].copy()
    print(f"  • Plottable GPS coordinate records: {len(geo_df):,}")

    # Center map on NYC coordinates
    nyc_center = [40.7128, -74.0060]

    # --- Map 1: Interactive Heatmap of All Complaints ---
    m_heat = folium.Map(
        location=nyc_center, zoom_start=11, tiles="CartoDB positron"
    )
    heat_data = geo_df[["latitude", "longitude"]].values.tolist()

    HeatMap(heat_data, radius=10, blur=15, max_zoom=1).add_to(m_heat)

    heat_map_path = os.path.join(output_dir, "nyc_complaint_heatmap.html")
    m_heat.save(heat_map_path)
    print(f"  ✅ Saved Heatmap to: {heat_map_path}")

    # --- Map 2: SLA Breach Cluster Map ---
    m_breach = folium.Map(
        location=nyc_center, zoom_start=11, tiles="CartoDB positron"
    )
    breach_df = geo_df[geo_df["is_sla_breached"] == 1].head(
        1000
    )  # Limit to 1000 points for browser performance

    marker_cluster = MarkerCluster().add_to(m_breach)

    for idx, row in breach_df.iterrows():
        popup_text = (
            f"<b>Category:</b> {row['complaint_type']}<br>"
            f"<b>Borough:</b> {row['borough']}<br>"
            f"<b>Resolution Time:</b> {row['resolution_time_hours']} hrs<br>"
            f"<b>SLA Target:</b> {row['sla_target_hours']} hrs"
        )
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=popup_text,
            icon=folium.Icon(color="red", icon="warning-sign"),
        ).add_to(marker_cluster)

    breach_map_path = os.path.join(output_dir, "sla_breach_hotspots.html")
    m_breach.save(breach_map_path)
    print(f"  ✅ Saved SLA Breach Cluster Map to: {breach_map_path}")


if __name__ == "__main__":
    generate_geo_hotspots()