<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" hasScaleBasedVisibilityFlag="0" minScale="1e+08" simplifyLocal="1" simplifyDrawingTol="1" simplifyMaxScale="1" simplifyAlgorithm="0" styleCategories="AllStyleCategories" version="3.10.1-A Coruña" labelsEnabled="1" simplifyDrawingHints="1" readOnly="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 attr="ALARM_LEV" forceraster="0" type="categorizedSymbol" enableorderby="0" symbollevels="0">
    <categories>
      <category label="Low Confidence" render="true" value="LOW" symbol="0"/>
      <category label="High Confidence" render="true" value="HIGH" symbol="1"/>
    </categories>
    <symbols>
      <symbol name="0" clip_to_extent="1" alpha="1" type="fill" force_rhr="0">
        <layer class="SimpleLine" locked="0" pass="0" enabled="1">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="255,238,1,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.5"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="1" clip_to_extent="1" alpha="1" type="fill" force_rhr="0">
        <layer class="SimpleLine" locked="0" pass="0" enabled="1">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="227,26,28,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.5"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <source-symbol>
      <symbol name="0" clip_to_extent="1" alpha="1" type="fill" force_rhr="0">
        <layer class="SimpleFill" locked="0" pass="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="175,10,112,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.26"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </source-symbol>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style fieldName="$id+1" fontUnderline="0" fontSize="8.25" blendMode="0" fontSizeUnit="Point" useSubstitutions="0" previewBkgrdColor="255,255,255,255" fontCapitals="0" isExpression="1" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontKerning="1" fontLetterSpacing="0" textOpacity="1" fontWeight="50" textColor="0,0,255,255" fontWordSpacing="0" fontStrikeout="0" namedStyle="Regular" fontFamily="MS Shell Dlg 2" multilineHeight="1" textOrientation="horizontal" fontItalic="0">
        <text-buffer bufferSizeUnits="MM" bufferDraw="1" bufferNoFill="0" bufferBlendMode="0" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferOpacity="1" bufferJoinStyle="128" bufferColor="255,255,255,255" bufferSize="1"/>
        <background shapeSizeType="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeSizeX="0" shapeRotation="0" shapeBorderColor="128,128,128,255" shapeOffsetX="0" shapeBlendMode="0" shapeJoinStyle="64" shapeDraw="0" shapeRadiiUnit="MM" shapeBorderWidth="0" shapeType="0" shapeRadiiY="0" shapeFillColor="255,255,255,255" shapeSizeY="0" shapeOffsetUnit="MM" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthUnit="MM" shapeSVGFile="" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeRotationType="0" shapeRadiiX="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeOpacity="1" shapeSizeUnit="MM" shapeOffsetY="0">
          <symbol name="markerSymbol" clip_to_extent="1" alpha="1" type="marker" force_rhr="0">
            <layer class="SimpleMarker" locked="0" pass="0" enabled="1">
              <prop k="angle" v="0"/>
              <prop k="color" v="141,90,153,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="circle"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="35,35,35,255"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="diameter"/>
              <prop k="size" v="2"/>
              <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties"/>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </background>
        <shadow shadowUnder="0" shadowOpacity="0.7" shadowScale="100" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowColor="0,0,0,255" shadowBlendMode="6" shadowRadius="1.5" shadowOffsetGlobal="1" shadowRadiusAlphaOnly="0" shadowRadiusUnit="MM" shadowOffsetAngle="135" shadowDraw="0" shadowOffsetUnit="MM" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetDist="1"/>
        <dd_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format addDirectionSymbol="0" decimals="3" leftDirectionSymbol="&lt;" rightDirectionSymbol=">" useMaxLineLengthForAutoWrap="1" multilineAlign="4294967295" formatNumbers="0" reverseDirectionSymbol="0" plussign="0" autoWrapLength="0" placeDirectionSymbol="0" wrapChar=""/>
      <placement xOffset="0" yOffset="0" layerType="PolygonGeometry" quadOffset="1" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" priority="5" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" offsetUnits="MapUnit" maxCurvedCharAngleOut="-25" distMapUnitScale="3x:0,0,0,0,0,0" overrunDistance="0" geometryGeneratorEnabled="0" centroidWhole="0" centroidInside="0" geometryGeneratorType="PointGeometry" fitInPolygonOnly="0" repeatDistance="0" repeatDistanceUnits="MM" overrunDistanceUnit="MM" offsetType="0" preserveRotation="1" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" distUnits="MM" geometryGenerator="" dist="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" placementFlags="10" rotationAngle="0" placement="1" maxCurvedCharAngleIn="25"/>
      <rendering scaleVisibility="0" minFeatureSize="0" drawLabels="1" obstacleType="0" maxNumLabels="2000" scaleMin="1" obstacle="1" scaleMax="10000000" mergeLines="0" zIndex="0" fontMinPixelSize="3" fontLimitPixelSize="0" obstacleFactor="1" limitNumLabels="0" upsidedownLabels="0" labelPerPart="0" fontMaxPixelSize="10000" displayAll="0"/>
      <dd_properties>
        <Option type="Map">
          <Option name="name" type="QString" value=""/>
          <Option name="properties"/>
          <Option name="type" type="QString" value="collection"/>
        </Option>
      </dd_properties>
      <callout type="simple">
        <Option type="Map">
          <Option name="anchorPoint" type="QString" value="pole_of_inaccessibility"/>
          <Option name="ddProperties" type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
          <Option name="drawToAllParts" type="bool" value="false"/>
          <Option name="enabled" type="QString" value="0"/>
          <Option name="lineSymbol" type="QString" value="&lt;symbol name=&quot;symbol&quot; clip_to_extent=&quot;1&quot; alpha=&quot;1&quot; type=&quot;line&quot; force_rhr=&quot;0&quot;>&lt;layer class=&quot;SimpleLine&quot; locked=&quot;0&quot; pass=&quot;0&quot; enabled=&quot;1&quot;>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; type=&quot;QString&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; type=&quot;QString&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>"/>
          <Option name="minLength" type="double" value="0"/>
          <Option name="minLengthMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
          <Option name="minLengthUnit" type="QString" value="MM"/>
          <Option name="offsetFromAnchor" type="double" value="0"/>
          <Option name="offsetFromAnchorMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
          <Option name="offsetFromAnchorUnit" type="QString" value="MM"/>
          <Option name="offsetFromLabel" type="double" value="0"/>
          <Option name="offsetFromLabelMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
          <Option name="offsetFromLabelUnit" type="QString" value="MM"/>
        </Option>
      </callout>
    </settings>
  </labeling>
  <customproperties>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory penAlpha="255" sizeType="MM" height="15" scaleDependency="Area" rotationOffset="270" sizeScale="3x:0,0,0,0,0,0" width="15" backgroundColor="#ffffff" backgroundAlpha="255" labelPlacementMethod="XHeight" opacity="1" minScaleDenominator="0" lineSizeType="MM" scaleBasedVisibility="0" minimumSize="0" penWidth="0" barWidth="5" enabled="0" diagramOrientation="Up" lineSizeScale="3x:0,0,0,0,0,0" maxScaleDenominator="1e+08" penColor="#000000">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" color="#000000" field=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings linePlacementFlags="2" obstacle="0" priority="0" dist="0" showAll="1" zIndex="0" placement="0">
    <properties>
      <Option type="Map">
        <Option name="name" type="QString" value=""/>
        <Option name="properties"/>
        <Option name="type" type="QString" value="collection"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration type="Map">
      <Option name="QgsGeometryGapCheck" type="Map">
        <Option name="allowedGapsBuffer" type="double" value="0"/>
        <Option name="allowedGapsEnabled" type="bool" value="false"/>
        <Option name="allowedGapsLayer" type="QString" value=""/>
      </Option>
    </checkConfiguration>
  </geometryOptions>
  <fieldConfiguration>
    <field name="LENGTH_KM">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="WIDTH_KM">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="BARIC_LAT">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="MIN_LAT">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="POSSIBLE_S">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="CLASS_VAL">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="REGION_AFF">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="MAX_LON">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="AREA_KM">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="COUNTRY_AS">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="MAX_LAT">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="MIN_LON">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="BARIC_LON">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ALARM_LEV">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="DATE-TIME">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="WSPDMIN">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="WSPDMAX">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="WSPDMEAN">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="WDIRMEAN">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="" field="LENGTH_KM"/>
    <alias index="1" name="" field="WIDTH_KM"/>
    <alias index="2" name="" field="BARIC_LAT"/>
    <alias index="3" name="" field="MIN_LAT"/>
    <alias index="4" name="" field="POSSIBLE_S"/>
    <alias index="5" name="" field="CLASS_VAL"/>
    <alias index="6" name="" field="REGION_AFF"/>
    <alias index="7" name="" field="MAX_LON"/>
    <alias index="8" name="" field="AREA_KM"/>
    <alias index="9" name="" field="COUNTRY_AS"/>
    <alias index="10" name="" field="MAX_LAT"/>
    <alias index="11" name="" field="MIN_LON"/>
    <alias index="12" name="" field="BARIC_LON"/>
    <alias index="13" name="" field="ALARM_LEV"/>
    <alias index="14" name="" field="DATE-TIME"/>
    <alias index="15" name="" field="WSPDMIN"/>
    <alias index="16" name="" field="WSPDMAX"/>
    <alias index="17" name="" field="WSPDMEAN"/>
    <alias index="18" name="" field="WDIRMEAN"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="LENGTH_KM" expression=""/>
    <default applyOnUpdate="0" field="WIDTH_KM" expression=""/>
    <default applyOnUpdate="0" field="BARIC_LAT" expression=""/>
    <default applyOnUpdate="0" field="MIN_LAT" expression=""/>
    <default applyOnUpdate="0" field="POSSIBLE_S" expression=""/>
    <default applyOnUpdate="0" field="CLASS_VAL" expression=""/>
    <default applyOnUpdate="0" field="REGION_AFF" expression=""/>
    <default applyOnUpdate="0" field="MAX_LON" expression=""/>
    <default applyOnUpdate="0" field="AREA_KM" expression=""/>
    <default applyOnUpdate="0" field="COUNTRY_AS" expression=""/>
    <default applyOnUpdate="0" field="MAX_LAT" expression=""/>
    <default applyOnUpdate="0" field="MIN_LON" expression=""/>
    <default applyOnUpdate="0" field="BARIC_LON" expression=""/>
    <default applyOnUpdate="0" field="ALARM_LEV" expression=""/>
    <default applyOnUpdate="0" field="DATE-TIME" expression=""/>
    <default applyOnUpdate="0" field="WSPDMIN" expression=""/>
    <default applyOnUpdate="0" field="WSPDMAX" expression=""/>
    <default applyOnUpdate="0" field="WSPDMEAN" expression=""/>
    <default applyOnUpdate="0" field="WDIRMEAN" expression=""/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" exp_strength="0" notnull_strength="0" field="LENGTH_KM" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" notnull_strength="0" field="WIDTH_KM" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" notnull_strength="0" field="BARIC_LAT" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" notnull_strength="0" field="MIN_LAT" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" notnull_strength="0" field="POSSIBLE_S" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" notnull_strength="0" field="CLASS_VAL" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" notnull_strength="0" field="REGION_AFF" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" notnull_strength="0" field="MAX_LON" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" notnull_strength="0" field="AREA_KM" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" notnull_strength="0" field="COUNTRY_AS" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" notnull_strength="0" field="MAX_LAT" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" notnull_strength="0" field="MIN_LON" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" notnull_strength="0" field="BARIC_LON" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" notnull_strength="0" field="ALARM_LEV" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" notnull_strength="0" field="DATE-TIME" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" notnull_strength="0" field="WSPDMIN" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" notnull_strength="0" field="WSPDMAX" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" notnull_strength="0" field="WSPDMEAN" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" notnull_strength="0" field="WDIRMEAN" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="LENGTH_KM" exp=""/>
    <constraint desc="" field="WIDTH_KM" exp=""/>
    <constraint desc="" field="BARIC_LAT" exp=""/>
    <constraint desc="" field="MIN_LAT" exp=""/>
    <constraint desc="" field="POSSIBLE_S" exp=""/>
    <constraint desc="" field="CLASS_VAL" exp=""/>
    <constraint desc="" field="REGION_AFF" exp=""/>
    <constraint desc="" field="MAX_LON" exp=""/>
    <constraint desc="" field="AREA_KM" exp=""/>
    <constraint desc="" field="COUNTRY_AS" exp=""/>
    <constraint desc="" field="MAX_LAT" exp=""/>
    <constraint desc="" field="MIN_LON" exp=""/>
    <constraint desc="" field="BARIC_LON" exp=""/>
    <constraint desc="" field="ALARM_LEV" exp=""/>
    <constraint desc="" field="DATE-TIME" exp=""/>
    <constraint desc="" field="WSPDMIN" exp=""/>
    <constraint desc="" field="WSPDMAX" exp=""/>
    <constraint desc="" field="WSPDMEAN" exp=""/>
    <constraint desc="" field="WDIRMEAN" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortExpression="" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column name="LENGTH_KM" hidden="0" type="field" width="-1"/>
      <column name="WIDTH_KM" hidden="0" type="field" width="-1"/>
      <column name="BARIC_LAT" hidden="0" type="field" width="-1"/>
      <column name="MIN_LAT" hidden="0" type="field" width="-1"/>
      <column name="POSSIBLE_S" hidden="0" type="field" width="-1"/>
      <column name="CLASS_VAL" hidden="0" type="field" width="-1"/>
      <column name="REGION_AFF" hidden="0" type="field" width="-1"/>
      <column name="MAX_LON" hidden="0" type="field" width="-1"/>
      <column name="AREA_KM" hidden="0" type="field" width="-1"/>
      <column name="COUNTRY_AS" hidden="0" type="field" width="-1"/>
      <column name="MAX_LAT" hidden="0" type="field" width="-1"/>
      <column name="MIN_LON" hidden="0" type="field" width="-1"/>
      <column name="BARIC_LON" hidden="0" type="field" width="-1"/>
      <column name="ALARM_LEV" hidden="0" type="field" width="-1"/>
      <column name="DATE-TIME" hidden="0" type="field" width="-1"/>
      <column hidden="1" type="actions" width="-1"/>
      <column name="WSPDMIN" hidden="0" type="field" width="-1"/>
      <column name="WSPDMAX" hidden="0" type="field" width="-1"/>
      <column name="WSPDMEAN" hidden="0" type="field" width="-1"/>
      <column name="WDIRMEAN" hidden="0" type="field" width="-1"/>
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
  <editforminitfilepath>D:/BARATA/2.seonse_outputs/sentinel/kepri_20181004_223936_oils</editforminitfilepath>
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
    <field name="ALARM_LEV" editable="1"/>
    <field name="AREA_KM" editable="1"/>
    <field name="BARIC_LAT" editable="1"/>
    <field name="BARIC_LON" editable="1"/>
    <field name="CLASS_VAL" editable="1"/>
    <field name="COUNTRY_AS" editable="1"/>
    <field name="DATE-TIME" editable="1"/>
    <field name="LENGTH_KM" editable="1"/>
    <field name="MAX_LAT" editable="1"/>
    <field name="MAX_LON" editable="1"/>
    <field name="MIN_LAT" editable="1"/>
    <field name="MIN_LON" editable="1"/>
    <field name="POSSIBLE_S" editable="1"/>
    <field name="REGION_AFF" editable="1"/>
    <field name="WDIRMEAN" editable="1"/>
    <field name="WIDTH_KM" editable="1"/>
    <field name="WSPDMAX" editable="1"/>
    <field name="WSPDMEAN" editable="1"/>
    <field name="WSPDMIN" editable="1"/>
    <field name="Wdir_mean" editable="1"/>
    <field name="Wspd_max" editable="1"/>
    <field name="Wspd_mean" editable="1"/>
    <field name="Wspd_min" editable="1"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="ALARM_LEV"/>
    <field labelOnTop="0" name="AREA_KM"/>
    <field labelOnTop="0" name="BARIC_LAT"/>
    <field labelOnTop="0" name="BARIC_LON"/>
    <field labelOnTop="0" name="CLASS_VAL"/>
    <field labelOnTop="0" name="COUNTRY_AS"/>
    <field labelOnTop="0" name="DATE-TIME"/>
    <field labelOnTop="0" name="LENGTH_KM"/>
    <field labelOnTop="0" name="MAX_LAT"/>
    <field labelOnTop="0" name="MAX_LON"/>
    <field labelOnTop="0" name="MIN_LAT"/>
    <field labelOnTop="0" name="MIN_LON"/>
    <field labelOnTop="0" name="POSSIBLE_S"/>
    <field labelOnTop="0" name="REGION_AFF"/>
    <field labelOnTop="0" name="WDIRMEAN"/>
    <field labelOnTop="0" name="WIDTH_KM"/>
    <field labelOnTop="0" name="WSPDMAX"/>
    <field labelOnTop="0" name="WSPDMEAN"/>
    <field labelOnTop="0" name="WSPDMIN"/>
    <field labelOnTop="0" name="Wdir_mean"/>
    <field labelOnTop="0" name="Wspd_max"/>
    <field labelOnTop="0" name="Wspd_mean"/>
    <field labelOnTop="0" name="Wspd_min"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>COALESCE( "WIDTH_KM", '&lt;NULL>' )</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
