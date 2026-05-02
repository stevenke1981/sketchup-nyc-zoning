"""FastMCP server exposing NYC zoning tools (stdio + HTTP transport)."""
import asyncio

from mcp.server.fastmcp import FastMCP

from nyczone_mcp.tools.get_borough_stats import get_borough_stats
from nyczone_mcp.tools.query_buildings import query_buildings
from nyczone_mcp.tools.query_pluto import query_pluto
from nyczone_mcp.tools.query_zoning_district import query_zoning_district
from nyczone_mcp.tools.search_by_address import search_by_address

mcp = FastMCP("nyc-zoning", instructions="Query NYC zoning, buildings, and PLUTO data.")

mcp.tool()(query_buildings)
mcp.tool()(query_zoning_district)
mcp.tool()(query_pluto)
mcp.tool()(search_by_address)
mcp.tool()(get_borough_stats)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
