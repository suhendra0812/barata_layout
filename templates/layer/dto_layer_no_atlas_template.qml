<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" simplifyAlgorithm="0" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyDrawingTol="1" simplifyDrawingHints="1" minScale="100000000" version="3.16.0-Hannover" labelsEnabled="0" styleCategories="AllStyleCategories" maxScale="0" simplifyLocal="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal startField="begin" accumulate="0" endField="end" endExpression="" enabled="0" durationUnit="min" startExpression="" durationField="" mode="0" fixedDuration="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 symbollevels="0" type="singleSymbol" enableorderby="0" forceraster="0">
    <symbols>
      <symbol clip_to_extent="1" force_rhr="0" type="fill" name="0" alpha="1">
        <layer class="SimpleLine" pass="0" enabled="1" locked="0">
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="215,25,28,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.5" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style fontLetterSpacing="0" previewBkgrdColor="255,255,255,255" fieldName="$id+1" capitalization="0" fontFamily="MS Shell Dlg 2" namedStyle="Regular" fontStrikeout="0" textColor="0,0,0,255" fontSizeUnit="Point" fontWeight="50" fontWordSpacing="0" allowHtml="0" blendMode="0" fontSize="10" fontUnderline="0" multilineHeight="1" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontItalic="0" fontKerning="1" textOpacity="1" textOrientation="horizontal" useSubstitutions="0" isExpression="1">
        <text-buffer bufferNoFill="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferBlendMode="0" bufferColor="255,255,255,255" bufferOpacity="1" bufferJoinStyle="128" bufferDraw="0" bufferSize="1" bufferSizeUnits="MM"/>
        <text-mask maskOpacity="1" maskSize="0" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskSizeUnits="MM" maskEnabled="0" maskType="0" maskJoinStyle="128" maskedSymbolLayers=""/>
        <background shapeSizeUnit="MM" shapeRadiiX="0" shapeSizeX="0" shapeRotationType="0" shapeBlendMode="0" shapeRadiiUnit="MM" shapeType="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeRotation="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthUnit="MM" shapeSVGFile="" shapeOffsetY="0" shapeOffsetUnit="MM" shapeBorderWidth="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderColor="128,128,128,255" shapeSizeType="0" shapeDraw="0" shapeRadiiY="0" shapeSizeY="0" shapeFillColor="255,255,255,255" shapeJoinStyle="64" shapeOpacity="1" shapeOffsetX="0">
          <symbol clip_to_extent="1" force_rhr="0" type="marker" name="markerSymbol" alpha="1">
            <layer class="SimpleMarker" pass="0" enabled="1" locked="0">
              <prop v="0" k="angle"/>
              <prop v="164,113,88,255" k="color"/>
              <prop v="1" k="horizontal_anchor_point"/>
              <prop v="bevel" k="joinstyle"/>
              <prop v="circle" k="name"/>
              <prop v="0,0" k="offset"/>
              <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
              <prop v="MM" k="offset_unit"/>
              <prop v="35,35,35,255" k="outline_color"/>
              <prop v="solid" k="outline_style"/>
              <prop v="0" k="outline_width"/>
              <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
              <prop v="MM" k="outline_width_unit"/>
              <prop v="diameter" k="scale_method"/>
              <prop v="2" k="size"/>
              <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
              <prop v="MM" k="size_unit"/>
              <prop v="1" k="vertical_anchor_point"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" type="QString" name="name"/>
                  <Option name="properties"/>
                  <Option value="collection" type="QString" name="type"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </background>
        <shadow shadowOffsetAngle="135" shadowOffsetGlobal="1" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowScale="100" shadowUnder="0" shadowBlendMode="6" shadowRadiusUnit="MM" shadowOpacity="0.7" shadowRadiusAlphaOnly="0" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadius="1.5" shadowOffsetDist="1" shadowOffsetUnit="MM" shadowDraw="0" shadowColor="0,0,0,255"/>
        <dd_properties>
          <Option type="Map">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format decimals="3" rightDirectionSymbol=">" plussign="0" reverseDirectionSymbol="0" autoWrapLength="0" multilineAlign="0" addDirectionSymbol="0" leftDirectionSymbol="&lt;" wrapChar="" formatNumbers="0" useMaxLineLengthForAutoWrap="1" placeDirectionSymbol="0"/>
      <placement priority="5" dist="0" fitInPolygonOnly="0" distMapUnitScale="3x:0,0,0,0,0,0" centroidWhole="0" layerType="PolygonGeometry" placement="0" maxCurvedCharAngleOut="-25" centroidInside="0" repeatDistanceUnits="MM" offsetUnits="MM" geometryGeneratorType="PointGeometry" yOffset="0" lineAnchorPercent="0.5" geometryGeneratorEnabled="0" rotationAngle="0" lineAnchorType="0" xOffset="0" polygonPlacementFlags="2" repeatDistance="0" quadOffset="4" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" distUnits="MM" maxCurvedCharAngleIn="25" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" preserveRotation="1" offsetType="0" geometryGenerator="" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" overrunDistance="0" placementFlags="10" overrunDistanceUnit="MM"/>
      <rendering zIndex="0" maxNumLabels="2000" fontMinPixelSize="3" minFeatureSize="0" displayAll="0" obstacle="1" fontMaxPixelSize="10000" drawLabels="1" upsidedownLabels="0" scaleVisibility="0" scaleMin="0" limitNumLabels="0" labelPerPart="0" obstacleFactor="1" fontLimitPixelSize="0" mergeLines="0" scaleMax="0" obstacleType="0"/>
      <dd_properties>
        <Option type="Map">
          <Option value="" type="QString" name="name"/>
          <Option name="properties"/>
          <Option value="collection" type="QString" name="type"/>
        </Option>
      </dd_properties>
      <callout type="simple">
        <Option type="Map">
          <Option value="pole_of_inaccessibility" type="QString" name="anchorPoint"/>
          <Option type="Map" name="ddProperties">
            <Option value="" type="QString" name="name"/>
            <Option name="properties"/>
            <Option value="collection" type="QString" name="type"/>
          </Option>
          <Option value="false" type="bool" name="drawToAllParts"/>
          <Option value="0" type="QString" name="enabled"/>
          <Option value="point_on_exterior" type="QString" name="labelAnchorPoint"/>
          <Option value="&lt;symbol clip_to_extent=&quot;1&quot; force_rhr=&quot;0&quot; type=&quot;line&quot; name=&quot;symbol&quot; alpha=&quot;1&quot;>&lt;layer class=&quot;SimpleLine&quot; pass=&quot;0&quot; enabled=&quot;1&quot; locked=&quot;0&quot;>&lt;prop v=&quot;0&quot; k=&quot;align_dash_pattern&quot;/>&lt;prop v=&quot;square&quot; k=&quot;capstyle&quot;/>&lt;prop v=&quot;5;2&quot; k=&quot;customdash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;customdash_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;customdash_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;dash_pattern_offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;dash_pattern_offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;dash_pattern_offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;draw_inside_polygon&quot;/>&lt;prop v=&quot;bevel&quot; k=&quot;joinstyle&quot;/>&lt;prop v=&quot;60,60,60,255&quot; k=&quot;line_color&quot;/>&lt;prop v=&quot;solid&quot; k=&quot;line_style&quot;/>&lt;prop v=&quot;0.3&quot; k=&quot;line_width&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;line_width_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;ring_filter&quot;/>&lt;prop v=&quot;0&quot; k=&quot;tweak_dash_pattern_on_corners&quot;/>&lt;prop v=&quot;0&quot; k=&quot;use_custom_dash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;width_map_unit_scale&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; type=&quot;QString&quot; name=&quot;name&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; type=&quot;QString&quot; name=&quot;type&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString" name="lineSymbol"/>
          <Option value="0" type="double" name="minLength"/>
          <Option value="3x:0,0,0,0,0,0" type="QString" name="minLengthMapUnitScale"/>
          <Option value="MM" type="QString" name="minLengthUnit"/>
          <Option value="0" type="double" name="offsetFromAnchor"/>
          <Option value="3x:0,0,0,0,0,0" type="QString" name="offsetFromAnchorMapUnitScale"/>
          <Option value="MM" type="QString" name="offsetFromAnchorUnit"/>
          <Option value="0" type="double" name="offsetFromLabel"/>
          <Option value="3x:0,0,0,0,0,0" type="QString" name="offsetFromLabelMapUnitScale"/>
          <Option value="MM" type="QString" name="offsetFromLabelUnit"/>
        </Option>
      </callout>
    </settings>
  </labeling>
  <customproperties>
    <property value="Name" key="dualview/previewExpressions"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory sizeScale="3x:0,0,0,0,0,0" backgroundColor="#ffffff" penWidth="0" lineSizeType="MM" enabled="0" width="15" scaleDependency="Area" diagramOrientation="Up" backgroundAlpha="255" direction="1" labelPlacementMethod="XHeight" opacity="1" spacingUnit="MM" spacing="0" lineSizeScale="3x:0,0,0,0,0,0" scaleBasedVisibility="0" minScaleDenominator="0" spacingUnitScale="3x:0,0,0,0,0,0" penAlpha="255" barWidth="5" minimumSize="0" penColor="#000000" sizeType="MM" showAxis="0" maxScaleDenominator="1e+08" height="15" rotationOffset="270">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute label="" field="" color="#000000"/>
      <axisSymbol>
        <symbol clip_to_extent="1" force_rhr="0" type="line" name="" alpha="1">
          <layer class="SimpleLine" pass="0" enabled="1" locked="0">
            <prop v="0" k="align_dash_pattern"/>
            <prop v="square" k="capstyle"/>
            <prop v="5;2" k="customdash"/>
            <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
            <prop v="MM" k="customdash_unit"/>
            <prop v="0" k="dash_pattern_offset"/>
            <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
            <prop v="MM" k="dash_pattern_offset_unit"/>
            <prop v="0" k="draw_inside_polygon"/>
            <prop v="bevel" k="joinstyle"/>
            <prop v="35,35,35,255" k="line_color"/>
            <prop v="solid" k="line_style"/>
            <prop v="0.26" k="line_width"/>
            <prop v="MM" k="line_width_unit"/>
            <prop v="0" k="offset"/>
            <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
            <prop v="MM" k="offset_unit"/>
            <prop v="0" k="ring_filter"/>
            <prop v="0" k="tweak_dash_pattern_on_corners"/>
            <prop v="0" k="use_custom_dash"/>
            <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
            <data_defined_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name"/>
                <Option name="properties"/>
                <Option value="collection" type="QString" name="type"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings priority="0" obstacle="0" dist="0" placement="1" showAll="1" linePlacementFlags="18" zIndex="0">
    <properties>
      <Option type="Map">
        <Option value="" type="QString" name="name"/>
        <Option name="properties"/>
        <Option value="collection" type="QString" name="type"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration type="Map">
      <Option type="Map" name="QgsGeometryGapCheck">
        <Option value="0" type="double" name="allowedGapsBuffer"/>
        <Option value="false" type="bool" name="allowedGapsEnabled"/>
        <Option value="" type="QString" name="allowedGapsLayer"/>
      </Option>
    </checkConfiguration>
  </geometryOptions>
  <legend type="default-vector"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field name="Name" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="description" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="timestamp" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="begin" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="end" configurationFlags="None">
      <editWidget type="DateTime">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="altitudeMode" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="tessellate" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="extrude" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="visibility" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="drawOrder" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="icon" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Albedo" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Altitude" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Anx" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="AnxLon" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="AreaCovered" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Azimuth" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="BetaAngle" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Center_Lat" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Center_Lat_AOI" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Center_Lon" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Center_Lon_AOI" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="CloudPercent" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Cost" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="CoverageId" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Cycle" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="DataSize" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Frame_End" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Frame_Start" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Frames" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Height" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="IntersectionArea" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="LandCover" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Length" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="LookAngle" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="MLST_End" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="MLST_Start" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Max_Incid" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Min_Incid" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="NE_Lat" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="NE_Lon" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="NW_Lat" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="NW_Lon" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="OZA" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="OrbName" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Orbit" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Pass" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Path" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Pitch" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Polarization" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Range" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Region" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="RelOrb" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Roll" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="SE_Lat" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="SE_Lon" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="SW_Lat" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="SW_Lon" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="SZA" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Satellite" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Sensor" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="SensorMode" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Slew" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="SpatialResolution" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="SunGlint" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="SwathArea" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="TargetInImage" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Width" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Yaw" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Date" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Start" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Duration" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Constellation" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="Name" name="" index="0"/>
    <alias field="description" name="" index="1"/>
    <alias field="timestamp" name="" index="2"/>
    <alias field="begin" name="" index="3"/>
    <alias field="end" name="" index="4"/>
    <alias field="altitudeMode" name="" index="5"/>
    <alias field="tessellate" name="" index="6"/>
    <alias field="extrude" name="" index="7"/>
    <alias field="visibility" name="" index="8"/>
    <alias field="drawOrder" name="" index="9"/>
    <alias field="icon" name="" index="10"/>
    <alias field="Albedo" name="" index="11"/>
    <alias field="Altitude" name="" index="12"/>
    <alias field="Anx" name="" index="13"/>
    <alias field="AnxLon" name="" index="14"/>
    <alias field="AreaCovered" name="" index="15"/>
    <alias field="Azimuth" name="" index="16"/>
    <alias field="BetaAngle" name="" index="17"/>
    <alias field="Center_Lat" name="" index="18"/>
    <alias field="Center_Lat_AOI" name="" index="19"/>
    <alias field="Center_Lon" name="" index="20"/>
    <alias field="Center_Lon_AOI" name="" index="21"/>
    <alias field="CloudPercent" name="" index="22"/>
    <alias field="Cost" name="" index="23"/>
    <alias field="CoverageId" name="" index="24"/>
    <alias field="Cycle" name="" index="25"/>
    <alias field="DataSize" name="" index="26"/>
    <alias field="Frame_End" name="" index="27"/>
    <alias field="Frame_Start" name="" index="28"/>
    <alias field="Frames" name="" index="29"/>
    <alias field="Height" name="" index="30"/>
    <alias field="IntersectionArea" name="" index="31"/>
    <alias field="LandCover" name="" index="32"/>
    <alias field="Length" name="" index="33"/>
    <alias field="LookAngle" name="" index="34"/>
    <alias field="MLST_End" name="" index="35"/>
    <alias field="MLST_Start" name="" index="36"/>
    <alias field="Max_Incid" name="" index="37"/>
    <alias field="Min_Incid" name="" index="38"/>
    <alias field="NE_Lat" name="" index="39"/>
    <alias field="NE_Lon" name="" index="40"/>
    <alias field="NW_Lat" name="" index="41"/>
    <alias field="NW_Lon" name="" index="42"/>
    <alias field="OZA" name="" index="43"/>
    <alias field="OrbName" name="" index="44"/>
    <alias field="Orbit" name="" index="45"/>
    <alias field="Pass" name="" index="46"/>
    <alias field="Path" name="" index="47"/>
    <alias field="Pitch" name="" index="48"/>
    <alias field="Polarization" name="" index="49"/>
    <alias field="Range" name="" index="50"/>
    <alias field="Region" name="" index="51"/>
    <alias field="RelOrb" name="" index="52"/>
    <alias field="Roll" name="" index="53"/>
    <alias field="SE_Lat" name="" index="54"/>
    <alias field="SE_Lon" name="" index="55"/>
    <alias field="SW_Lat" name="" index="56"/>
    <alias field="SW_Lon" name="" index="57"/>
    <alias field="SZA" name="" index="58"/>
    <alias field="Satellite" name="" index="59"/>
    <alias field="Sensor" name="" index="60"/>
    <alias field="SensorMode" name="" index="61"/>
    <alias field="Slew" name="" index="62"/>
    <alias field="SpatialResolution" name="" index="63"/>
    <alias field="SunGlint" name="" index="64"/>
    <alias field="SwathArea" name="" index="65"/>
    <alias field="TargetInImage" name="" index="66"/>
    <alias field="Width" name="" index="67"/>
    <alias field="Yaw" name="" index="68"/>
    <alias field="Date" name="" index="69"/>
    <alias field="Start" name="" index="70"/>
    <alias field="Duration" name="" index="71"/>
    <alias field="Constellation" name="" index="72"/>
  </aliases>
  <defaults>
    <default field="Name" applyOnUpdate="0" expression=""/>
    <default field="description" applyOnUpdate="0" expression=""/>
    <default field="timestamp" applyOnUpdate="0" expression=""/>
    <default field="begin" applyOnUpdate="0" expression=""/>
    <default field="end" applyOnUpdate="0" expression=""/>
    <default field="altitudeMode" applyOnUpdate="0" expression=""/>
    <default field="tessellate" applyOnUpdate="0" expression=""/>
    <default field="extrude" applyOnUpdate="0" expression=""/>
    <default field="visibility" applyOnUpdate="0" expression=""/>
    <default field="drawOrder" applyOnUpdate="0" expression=""/>
    <default field="icon" applyOnUpdate="0" expression=""/>
    <default field="Albedo" applyOnUpdate="0" expression=""/>
    <default field="Altitude" applyOnUpdate="0" expression=""/>
    <default field="Anx" applyOnUpdate="0" expression=""/>
    <default field="AnxLon" applyOnUpdate="0" expression=""/>
    <default field="AreaCovered" applyOnUpdate="0" expression=""/>
    <default field="Azimuth" applyOnUpdate="0" expression=""/>
    <default field="BetaAngle" applyOnUpdate="0" expression=""/>
    <default field="Center_Lat" applyOnUpdate="0" expression=""/>
    <default field="Center_Lat_AOI" applyOnUpdate="0" expression=""/>
    <default field="Center_Lon" applyOnUpdate="0" expression=""/>
    <default field="Center_Lon_AOI" applyOnUpdate="0" expression=""/>
    <default field="CloudPercent" applyOnUpdate="0" expression=""/>
    <default field="Cost" applyOnUpdate="0" expression=""/>
    <default field="CoverageId" applyOnUpdate="0" expression=""/>
    <default field="Cycle" applyOnUpdate="0" expression=""/>
    <default field="DataSize" applyOnUpdate="0" expression=""/>
    <default field="Frame_End" applyOnUpdate="0" expression=""/>
    <default field="Frame_Start" applyOnUpdate="0" expression=""/>
    <default field="Frames" applyOnUpdate="0" expression=""/>
    <default field="Height" applyOnUpdate="0" expression=""/>
    <default field="IntersectionArea" applyOnUpdate="0" expression=""/>
    <default field="LandCover" applyOnUpdate="0" expression=""/>
    <default field="Length" applyOnUpdate="0" expression=""/>
    <default field="LookAngle" applyOnUpdate="0" expression=""/>
    <default field="MLST_End" applyOnUpdate="0" expression=""/>
    <default field="MLST_Start" applyOnUpdate="0" expression=""/>
    <default field="Max_Incid" applyOnUpdate="0" expression=""/>
    <default field="Min_Incid" applyOnUpdate="0" expression=""/>
    <default field="NE_Lat" applyOnUpdate="0" expression=""/>
    <default field="NE_Lon" applyOnUpdate="0" expression=""/>
    <default field="NW_Lat" applyOnUpdate="0" expression=""/>
    <default field="NW_Lon" applyOnUpdate="0" expression=""/>
    <default field="OZA" applyOnUpdate="0" expression=""/>
    <default field="OrbName" applyOnUpdate="0" expression=""/>
    <default field="Orbit" applyOnUpdate="0" expression=""/>
    <default field="Pass" applyOnUpdate="0" expression=""/>
    <default field="Path" applyOnUpdate="0" expression=""/>
    <default field="Pitch" applyOnUpdate="0" expression=""/>
    <default field="Polarization" applyOnUpdate="0" expression=""/>
    <default field="Range" applyOnUpdate="0" expression=""/>
    <default field="Region" applyOnUpdate="0" expression=""/>
    <default field="RelOrb" applyOnUpdate="0" expression=""/>
    <default field="Roll" applyOnUpdate="0" expression=""/>
    <default field="SE_Lat" applyOnUpdate="0" expression=""/>
    <default field="SE_Lon" applyOnUpdate="0" expression=""/>
    <default field="SW_Lat" applyOnUpdate="0" expression=""/>
    <default field="SW_Lon" applyOnUpdate="0" expression=""/>
    <default field="SZA" applyOnUpdate="0" expression=""/>
    <default field="Satellite" applyOnUpdate="0" expression=""/>
    <default field="Sensor" applyOnUpdate="0" expression=""/>
    <default field="SensorMode" applyOnUpdate="0" expression=""/>
    <default field="Slew" applyOnUpdate="0" expression=""/>
    <default field="SpatialResolution" applyOnUpdate="0" expression=""/>
    <default field="SunGlint" applyOnUpdate="0" expression=""/>
    <default field="SwathArea" applyOnUpdate="0" expression=""/>
    <default field="TargetInImage" applyOnUpdate="0" expression=""/>
    <default field="Width" applyOnUpdate="0" expression=""/>
    <default field="Yaw" applyOnUpdate="0" expression=""/>
    <default field="Date" applyOnUpdate="0" expression=""/>
    <default field="Start" applyOnUpdate="0" expression=""/>
    <default field="Duration" applyOnUpdate="0" expression=""/>
    <default field="Constellation" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Name" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="description" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="timestamp" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="begin" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="end" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="altitudeMode" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="tessellate" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="extrude" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="visibility" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="drawOrder" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="icon" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Albedo" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Altitude" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Anx" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="AnxLon" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="AreaCovered" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Azimuth" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="BetaAngle" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Center_Lat" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Center_Lat_AOI" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Center_Lon" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Center_Lon_AOI" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="CloudPercent" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Cost" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="CoverageId" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Cycle" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="DataSize" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Frame_End" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Frame_Start" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Frames" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Height" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="IntersectionArea" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="LandCover" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Length" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="LookAngle" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="MLST_End" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="MLST_Start" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Max_Incid" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Min_Incid" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="NE_Lat" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="NE_Lon" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="NW_Lat" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="NW_Lon" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="OZA" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="OrbName" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Orbit" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Pass" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Path" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Pitch" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Polarization" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Range" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Region" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="RelOrb" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Roll" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="SE_Lat" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="SE_Lon" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="SW_Lat" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="SW_Lon" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="SZA" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Satellite" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Sensor" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="SensorMode" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Slew" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="SpatialResolution" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="SunGlint" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="SwathArea" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="TargetInImage" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Width" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Yaw" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Date" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Start" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Duration" exp_strength="0"/>
    <constraint notnull_strength="0" constraints="0" unique_strength="0" field="Constellation" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="Name" desc=""/>
    <constraint exp="" field="description" desc=""/>
    <constraint exp="" field="timestamp" desc=""/>
    <constraint exp="" field="begin" desc=""/>
    <constraint exp="" field="end" desc=""/>
    <constraint exp="" field="altitudeMode" desc=""/>
    <constraint exp="" field="tessellate" desc=""/>
    <constraint exp="" field="extrude" desc=""/>
    <constraint exp="" field="visibility" desc=""/>
    <constraint exp="" field="drawOrder" desc=""/>
    <constraint exp="" field="icon" desc=""/>
    <constraint exp="" field="Albedo" desc=""/>
    <constraint exp="" field="Altitude" desc=""/>
    <constraint exp="" field="Anx" desc=""/>
    <constraint exp="" field="AnxLon" desc=""/>
    <constraint exp="" field="AreaCovered" desc=""/>
    <constraint exp="" field="Azimuth" desc=""/>
    <constraint exp="" field="BetaAngle" desc=""/>
    <constraint exp="" field="Center_Lat" desc=""/>
    <constraint exp="" field="Center_Lat_AOI" desc=""/>
    <constraint exp="" field="Center_Lon" desc=""/>
    <constraint exp="" field="Center_Lon_AOI" desc=""/>
    <constraint exp="" field="CloudPercent" desc=""/>
    <constraint exp="" field="Cost" desc=""/>
    <constraint exp="" field="CoverageId" desc=""/>
    <constraint exp="" field="Cycle" desc=""/>
    <constraint exp="" field="DataSize" desc=""/>
    <constraint exp="" field="Frame_End" desc=""/>
    <constraint exp="" field="Frame_Start" desc=""/>
    <constraint exp="" field="Frames" desc=""/>
    <constraint exp="" field="Height" desc=""/>
    <constraint exp="" field="IntersectionArea" desc=""/>
    <constraint exp="" field="LandCover" desc=""/>
    <constraint exp="" field="Length" desc=""/>
    <constraint exp="" field="LookAngle" desc=""/>
    <constraint exp="" field="MLST_End" desc=""/>
    <constraint exp="" field="MLST_Start" desc=""/>
    <constraint exp="" field="Max_Incid" desc=""/>
    <constraint exp="" field="Min_Incid" desc=""/>
    <constraint exp="" field="NE_Lat" desc=""/>
    <constraint exp="" field="NE_Lon" desc=""/>
    <constraint exp="" field="NW_Lat" desc=""/>
    <constraint exp="" field="NW_Lon" desc=""/>
    <constraint exp="" field="OZA" desc=""/>
    <constraint exp="" field="OrbName" desc=""/>
    <constraint exp="" field="Orbit" desc=""/>
    <constraint exp="" field="Pass" desc=""/>
    <constraint exp="" field="Path" desc=""/>
    <constraint exp="" field="Pitch" desc=""/>
    <constraint exp="" field="Polarization" desc=""/>
    <constraint exp="" field="Range" desc=""/>
    <constraint exp="" field="Region" desc=""/>
    <constraint exp="" field="RelOrb" desc=""/>
    <constraint exp="" field="Roll" desc=""/>
    <constraint exp="" field="SE_Lat" desc=""/>
    <constraint exp="" field="SE_Lon" desc=""/>
    <constraint exp="" field="SW_Lat" desc=""/>
    <constraint exp="" field="SW_Lon" desc=""/>
    <constraint exp="" field="SZA" desc=""/>
    <constraint exp="" field="Satellite" desc=""/>
    <constraint exp="" field="Sensor" desc=""/>
    <constraint exp="" field="SensorMode" desc=""/>
    <constraint exp="" field="Slew" desc=""/>
    <constraint exp="" field="SpatialResolution" desc=""/>
    <constraint exp="" field="SunGlint" desc=""/>
    <constraint exp="" field="SwathArea" desc=""/>
    <constraint exp="" field="TargetInImage" desc=""/>
    <constraint exp="" field="Width" desc=""/>
    <constraint exp="" field="Yaw" desc=""/>
    <constraint exp="" field="Date" desc=""/>
    <constraint exp="" field="Start" desc=""/>
    <constraint exp="" field="Duration" desc=""/>
    <constraint exp="" field="Constellation" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column type="actions" width="-1" hidden="1"/>
      <column type="field" name="Satellite" width="-1" hidden="0"/>
      <column type="field" name="Name" width="-1" hidden="0"/>
      <column type="field" name="description" width="-1" hidden="0"/>
      <column type="field" name="timestamp" width="-1" hidden="0"/>
      <column type="field" name="begin" width="-1" hidden="0"/>
      <column type="field" name="end" width="-1" hidden="0"/>
      <column type="field" name="altitudeMode" width="-1" hidden="0"/>
      <column type="field" name="tessellate" width="-1" hidden="0"/>
      <column type="field" name="extrude" width="-1" hidden="0"/>
      <column type="field" name="visibility" width="-1" hidden="0"/>
      <column type="field" name="drawOrder" width="-1" hidden="0"/>
      <column type="field" name="icon" width="-1" hidden="0"/>
      <column type="field" name="Albedo" width="-1" hidden="0"/>
      <column type="field" name="Altitude" width="-1" hidden="0"/>
      <column type="field" name="Anx" width="-1" hidden="0"/>
      <column type="field" name="AnxLon" width="-1" hidden="0"/>
      <column type="field" name="AreaCovered" width="-1" hidden="0"/>
      <column type="field" name="Azimuth" width="-1" hidden="0"/>
      <column type="field" name="BetaAngle" width="-1" hidden="0"/>
      <column type="field" name="Center_Lat" width="-1" hidden="0"/>
      <column type="field" name="Center_Lat_AOI" width="-1" hidden="0"/>
      <column type="field" name="Center_Lon" width="-1" hidden="0"/>
      <column type="field" name="Center_Lon_AOI" width="-1" hidden="0"/>
      <column type="field" name="CloudPercent" width="-1" hidden="0"/>
      <column type="field" name="Cost" width="-1" hidden="0"/>
      <column type="field" name="CoverageId" width="-1" hidden="0"/>
      <column type="field" name="Cycle" width="-1" hidden="0"/>
      <column type="field" name="DataSize" width="-1" hidden="0"/>
      <column type="field" name="Frame_End" width="-1" hidden="0"/>
      <column type="field" name="Frame_Start" width="-1" hidden="0"/>
      <column type="field" name="Frames" width="-1" hidden="0"/>
      <column type="field" name="Height" width="-1" hidden="0"/>
      <column type="field" name="IntersectionArea" width="-1" hidden="0"/>
      <column type="field" name="LandCover" width="-1" hidden="0"/>
      <column type="field" name="Length" width="-1" hidden="0"/>
      <column type="field" name="LookAngle" width="-1" hidden="0"/>
      <column type="field" name="MLST_End" width="-1" hidden="0"/>
      <column type="field" name="MLST_Start" width="-1" hidden="0"/>
      <column type="field" name="Max_Incid" width="-1" hidden="0"/>
      <column type="field" name="Min_Incid" width="-1" hidden="0"/>
      <column type="field" name="NE_Lat" width="-1" hidden="0"/>
      <column type="field" name="NE_Lon" width="-1" hidden="0"/>
      <column type="field" name="NW_Lat" width="-1" hidden="0"/>
      <column type="field" name="NW_Lon" width="-1" hidden="0"/>
      <column type="field" name="OZA" width="-1" hidden="0"/>
      <column type="field" name="OrbName" width="-1" hidden="0"/>
      <column type="field" name="Orbit" width="-1" hidden="0"/>
      <column type="field" name="Pass" width="-1" hidden="0"/>
      <column type="field" name="Path" width="-1" hidden="0"/>
      <column type="field" name="Pitch" width="-1" hidden="0"/>
      <column type="field" name="Polarization" width="-1" hidden="0"/>
      <column type="field" name="Range" width="-1" hidden="0"/>
      <column type="field" name="Region" width="-1" hidden="0"/>
      <column type="field" name="RelOrb" width="-1" hidden="0"/>
      <column type="field" name="Roll" width="-1" hidden="0"/>
      <column type="field" name="SE_Lat" width="-1" hidden="0"/>
      <column type="field" name="SE_Lon" width="-1" hidden="0"/>
      <column type="field" name="SW_Lat" width="-1" hidden="0"/>
      <column type="field" name="SW_Lon" width="-1" hidden="0"/>
      <column type="field" name="SZA" width="-1" hidden="0"/>
      <column type="field" name="Sensor" width="-1" hidden="0"/>
      <column type="field" name="SensorMode" width="-1" hidden="0"/>
      <column type="field" name="Slew" width="-1" hidden="0"/>
      <column type="field" name="SpatialResolution" width="-1" hidden="0"/>
      <column type="field" name="SunGlint" width="-1" hidden="0"/>
      <column type="field" name="SwathArea" width="-1" hidden="0"/>
      <column type="field" name="TargetInImage" width="-1" hidden="0"/>
      <column type="field" name="Width" width="-1" hidden="0"/>
      <column type="field" name="Yaw" width="-1" hidden="0"/>
      <column type="field" name="Date" width="-1" hidden="0"/>
      <column type="field" name="Start" width="-1" hidden="0"/>
      <column type="field" name="Duration" width="-1" hidden="0"/>
      <column type="field" name="Constellation" width="-1" hidden="0"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field editable="1" name="Albedo"/>
    <field editable="1" name="Altitude"/>
    <field editable="1" name="Anx"/>
    <field editable="1" name="AnxLon"/>
    <field editable="1" name="AreaCovered"/>
    <field editable="1" name="Azimuth"/>
    <field editable="1" name="Beam"/>
    <field editable="1" name="BetaAngle"/>
    <field editable="1" name="Center_Lat"/>
    <field editable="1" name="Center_Lat_AOI"/>
    <field editable="1" name="Center_Lon"/>
    <field editable="1" name="Center_Lon_AOI"/>
    <field editable="1" name="CloudPercent"/>
    <field editable="1" name="Constellation"/>
    <field editable="1" name="Cost"/>
    <field editable="1" name="CoverageId"/>
    <field editable="1" name="Cycle"/>
    <field editable="1" name="DataSize"/>
    <field editable="1" name="Date"/>
    <field editable="1" name="Datetime"/>
    <field editable="1" name="Direction"/>
    <field editable="1" name="Duration"/>
    <field editable="1" name="Frame_End"/>
    <field editable="1" name="Frame_Start"/>
    <field editable="1" name="Frames"/>
    <field editable="1" name="Height"/>
    <field editable="1" name="IntersectionArea"/>
    <field editable="1" name="LandCover"/>
    <field editable="1" name="Length"/>
    <field editable="1" name="Look Angle"/>
    <field editable="1" name="Look Side"/>
    <field editable="1" name="LookAngle"/>
    <field editable="1" name="MLST_End"/>
    <field editable="1" name="MLST_Start"/>
    <field editable="1" name="Max_Incid"/>
    <field editable="1" name="Min_Incid"/>
    <field editable="1" name="Mode"/>
    <field editable="1" name="NE_Lat"/>
    <field editable="1" name="NE_Lon"/>
    <field editable="1" name="NW_Lat"/>
    <field editable="1" name="NW_Lon"/>
    <field editable="1" name="Name"/>
    <field editable="1" name="OZA"/>
    <field editable="1" name="OrbName"/>
    <field editable="1" name="Orbit"/>
    <field editable="1" name="Pass"/>
    <field editable="1" name="Path"/>
    <field editable="1" name="Pitch"/>
    <field editable="1" name="Polarization"/>
    <field editable="1" name="Range"/>
    <field editable="1" name="Region"/>
    <field editable="1" name="RelOrb"/>
    <field editable="1" name="Roll"/>
    <field editable="1" name="SE_Lat"/>
    <field editable="1" name="SE_Lon"/>
    <field editable="1" name="SW_Lat"/>
    <field editable="1" name="SW_Lon"/>
    <field editable="1" name="SZA"/>
    <field editable="1" name="Satellite"/>
    <field editable="1" name="Sensor"/>
    <field editable="1" name="SensorMode"/>
    <field editable="1" name="Slew"/>
    <field editable="1" name="SpatialResolution"/>
    <field editable="1" name="Start"/>
    <field editable="1" name="Start Time"/>
    <field editable="1" name="Stop Time"/>
    <field editable="1" name="SunGlint"/>
    <field editable="1" name="SwathArea"/>
    <field editable="1" name="TargetInImage"/>
    <field editable="1" name="Width"/>
    <field editable="1" name="Yaw"/>
    <field editable="1" name="altitudeMo"/>
    <field editable="1" name="altitudeMode"/>
    <field editable="1" name="begin"/>
    <field editable="1" name="descriptio"/>
    <field editable="1" name="description"/>
    <field editable="1" name="drawOrder"/>
    <field editable="1" name="end"/>
    <field editable="1" name="extrude"/>
    <field editable="1" name="icon"/>
    <field editable="1" name="id"/>
    <field editable="1" name="tessellate"/>
    <field editable="1" name="timestamp"/>
    <field editable="1" name="visibility"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="Albedo"/>
    <field labelOnTop="0" name="Altitude"/>
    <field labelOnTop="0" name="Anx"/>
    <field labelOnTop="0" name="AnxLon"/>
    <field labelOnTop="0" name="AreaCovered"/>
    <field labelOnTop="0" name="Azimuth"/>
    <field labelOnTop="0" name="Beam"/>
    <field labelOnTop="0" name="BetaAngle"/>
    <field labelOnTop="0" name="Center_Lat"/>
    <field labelOnTop="0" name="Center_Lat_AOI"/>
    <field labelOnTop="0" name="Center_Lon"/>
    <field labelOnTop="0" name="Center_Lon_AOI"/>
    <field labelOnTop="0" name="CloudPercent"/>
    <field labelOnTop="0" name="Constellation"/>
    <field labelOnTop="0" name="Cost"/>
    <field labelOnTop="0" name="CoverageId"/>
    <field labelOnTop="0" name="Cycle"/>
    <field labelOnTop="0" name="DataSize"/>
    <field labelOnTop="0" name="Date"/>
    <field labelOnTop="0" name="Datetime"/>
    <field labelOnTop="0" name="Direction"/>
    <field labelOnTop="0" name="Duration"/>
    <field labelOnTop="0" name="Frame_End"/>
    <field labelOnTop="0" name="Frame_Start"/>
    <field labelOnTop="0" name="Frames"/>
    <field labelOnTop="0" name="Height"/>
    <field labelOnTop="0" name="IntersectionArea"/>
    <field labelOnTop="0" name="LandCover"/>
    <field labelOnTop="0" name="Length"/>
    <field labelOnTop="0" name="Look Angle"/>
    <field labelOnTop="0" name="Look Side"/>
    <field labelOnTop="0" name="LookAngle"/>
    <field labelOnTop="0" name="MLST_End"/>
    <field labelOnTop="0" name="MLST_Start"/>
    <field labelOnTop="0" name="Max_Incid"/>
    <field labelOnTop="0" name="Min_Incid"/>
    <field labelOnTop="0" name="Mode"/>
    <field labelOnTop="0" name="NE_Lat"/>
    <field labelOnTop="0" name="NE_Lon"/>
    <field labelOnTop="0" name="NW_Lat"/>
    <field labelOnTop="0" name="NW_Lon"/>
    <field labelOnTop="0" name="Name"/>
    <field labelOnTop="0" name="OZA"/>
    <field labelOnTop="0" name="OrbName"/>
    <field labelOnTop="0" name="Orbit"/>
    <field labelOnTop="0" name="Pass"/>
    <field labelOnTop="0" name="Path"/>
    <field labelOnTop="0" name="Pitch"/>
    <field labelOnTop="0" name="Polarization"/>
    <field labelOnTop="0" name="Range"/>
    <field labelOnTop="0" name="Region"/>
    <field labelOnTop="0" name="RelOrb"/>
    <field labelOnTop="0" name="Roll"/>
    <field labelOnTop="0" name="SE_Lat"/>
    <field labelOnTop="0" name="SE_Lon"/>
    <field labelOnTop="0" name="SW_Lat"/>
    <field labelOnTop="0" name="SW_Lon"/>
    <field labelOnTop="0" name="SZA"/>
    <field labelOnTop="0" name="Satellite"/>
    <field labelOnTop="0" name="Sensor"/>
    <field labelOnTop="0" name="SensorMode"/>
    <field labelOnTop="0" name="Slew"/>
    <field labelOnTop="0" name="SpatialResolution"/>
    <field labelOnTop="0" name="Start"/>
    <field labelOnTop="0" name="Start Time"/>
    <field labelOnTop="0" name="Stop Time"/>
    <field labelOnTop="0" name="SunGlint"/>
    <field labelOnTop="0" name="SwathArea"/>
    <field labelOnTop="0" name="TargetInImage"/>
    <field labelOnTop="0" name="Width"/>
    <field labelOnTop="0" name="Yaw"/>
    <field labelOnTop="0" name="altitudeMo"/>
    <field labelOnTop="0" name="altitudeMode"/>
    <field labelOnTop="0" name="begin"/>
    <field labelOnTop="0" name="descriptio"/>
    <field labelOnTop="0" name="description"/>
    <field labelOnTop="0" name="drawOrder"/>
    <field labelOnTop="0" name="end"/>
    <field labelOnTop="0" name="extrude"/>
    <field labelOnTop="0" name="icon"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="tessellate"/>
    <field labelOnTop="0" name="timestamp"/>
    <field labelOnTop="0" name="visibility"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"Name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
