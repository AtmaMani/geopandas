import os

import pandas as pd
try:
    from arcgis.features import GeoAccessor, GeoSeriesAccessor
    skip_ags_tests=False
except ImportError:
    skip_ags_tests=True
    pass
import pytest
from shapely.geometry import Point, Polygon, box

import geopandas
from geopandas import GeoDataFrame, read_file
from geopandas.testing import assert_geodataframe_equal, assert_geoseries_equal
from geopandas.tests.util import PACKAGE_DIR, validate_boro_df

@pytest.fixture
def df_nybb():
    nybb_path = geopandas.datasets.get_path("nybb")
    df = read_file(nybb_path)
    return df

@pytest.fixture
def df_null():
    return read_file(os.path.join(PACKAGE_DIR, "examples", "null_geom.geojson"))

@pytest.fixture
def df_points():
    N = 10
    crs = {"init": "epsg:4326"}
    df = GeoDataFrame(
        [
            {"geometry": Point(x, y), "value1": x + y, "value2": x * y}
            for x, y in zip(range(N), range(N))
        ],
        crs=crs,
    )
    return df


# -----------------------------------------------------------------------------
# to_arcgis_sedf tests
# -----------------------------------------------------------------------------

@pytest.mark.skipif(skip_ags_tests, reason="ArcGIS conda pkg needed")
def test_to_arcgis_sedf_sanity():
    # get NY GeoDataFrame
    ny_gdf = df_nybb()

    # convert to ArcGIS Spatially Enabled DataFrame obj
    ny_sedf = ny_gdf.to_arcgis_sedf()

    # assert instance type
    assert isinstance(ny_sedf, pd.DataFrame)

    # assert presence of SHAPE column
    assert 'SHAPE' in ny_sedf.columns

# -----------------------------------------------------------------------------
# from_arcgis_sedf tests
# -----------------------------------------------------------------------------
@pytest.mark.skipif(skip_ags_tests, reason="ArcGIS conda pkg needed")
def test_from_arcgis_sedf_sanity():
    # get NY shape file path
    ny_shp = geopandas.datasets.get_path('nybb')

    # read into SeDF
    ny_sedf = pd.DataFrame.spatial.from_featureclass(ny_shp)

    # convert SeDF to GDF
    ny_gdf = GeoDataFrame.read_arcgis_sedf(ny_sedf)

    # assert instance type
    assert isinstance(ny_gdf, GeoDataFrame)
