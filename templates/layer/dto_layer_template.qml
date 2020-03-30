<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" version="3.10.2-A Coruña" minScale="1e+08" simplifyLocal="1" simplifyMaxScale="1" labelsEnabled="1" hasScaleBasedVisibilityFlag="0" maxScale="0" simplifyDrawingTol="1" readOnly="0" simplifyDrawingHints="1" simplifyAlgorithm="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" type="RuleRenderer" symbollevels="0" enableorderby="0">
    <rules key="{1683a190-adbf-40aa-81d6-5d2c7a263b39}">
      <rule label="DTO" symbol="0" key="{9eb1e871-e0d3-4f15-b54c-1f9dcf166a57}" filter="$id = @atlas_featureid"/>
      <rule label="ELSE" key="{db4f6359-9984-43c6-bf0f-299a74a32b35}" filter="ELSE"/>
    </rules>
    <symbols>
      <symbol name="0" alpha="1" clip_to_extent="1" type="fill" force_rhr="0">
        <layer locked="0" class="SimpleLine" enabled="1" pass="0">
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
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
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <labeling type="rule-based">
    <rules key="{b05761ee-5b8a-472f-bf66-b9aaf4e1f3d0}">
      <rule key="{c218f374-756e-4f5f-bd4b-6451ae681227}" filter="$id+1">
        <settings calloutType="simple">
          <text-style blendMode="0" fontStrikeout="0" fontSize="10" fontSizeUnit="Point" fontItalic="0" fontKerning="1" fontSizeMapUnitScale="3x:0,0,0,0,0,0" namedStyle="Regular" textOrientation="horizontal" textOpacity="1" previewBkgrdColor="255,255,255,255" fontWordSpacing="0" fontLetterSpacing="0" fontFamily="MS Shell Dlg 2" fontUnderline="0" textColor="0,0,0,255" fieldName=" @layer_name || day(to_datetime(&quot;Datetime&quot;) + to_interval('7 hours'))" isExpression="1" fontWeight="50" useSubstitutions="0" multilineHeight="1" fontCapitals="0">
            <text-buffer bufferColor="255,255,255,255" bufferDraw="0" bufferOpacity="1" bufferBlendMode="0" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferNoFill="1" bufferSizeUnits="MM" bufferJoinStyle="128" bufferSize="1"/>
            <background shapeSizeType="0" shapeBorderWidthUnit="MM" shapeJoinStyle="64" shapeOpacity="1" shapeFillColor="255,255,255,255" shapeRadiiUnit="MM" shapeOffsetX="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiX="0" shapeSizeY="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeType="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeDraw="0" shapeSizeUnit="MM" shapeOffsetUnit="MM" shapeRadiiY="0" shapeBorderColor="128,128,128,255" shapeBorderWidth="0" shapeSizeX="0" shapeSVGFile="" shapeRotationType="0" shapeOffsetY="0" shapeRotation="0" shapeBlendMode="0">
              <symbol name="markerSymbol" alpha="1" clip_to_extent="1" type="marker" force_rhr="0">
                <layer locked="0" class="SimpleMarker" enabled="1" pass="0">
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
                      <Option name="name" value="" type="QString"/>
                      <Option name="properties"/>
                      <Option name="type" value="collection" type="QString"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </background>
            <shadow shadowRadius="1.5" shadowRadiusAlphaOnly="0" shadowOffsetUnit="MM" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetGlobal="1" shadowOffsetAngle="135" shadowUnder="0" shadowScale="100" shadowBlendMode="6" shadowOpacity="0.7" shadowDraw="0" shadowOffsetDist="1" shadowColor="0,0,0,255" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusUnit="MM"/>
            <dd_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format addDirectionSymbol="0" autoWrapLength="0" useMaxLineLengthForAutoWrap="1" reverseDirectionSymbol="0" formatNumbers="0" wrapChar="" rightDirectionSymbol=">" multilineAlign="0" placeDirectionSymbol="0" decimals="3" plussign="0" leftDirectionSymbol="&lt;"/>
          <placement fitInPolygonOnly="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorType="PointGeometry" preserveRotation="1" maxCurvedCharAngleOut="-25" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" placementFlags="10" quadOffset="4" centroidInside="0" rotationAngle="0" yOffset="0" placement="0" distUnits="MM" offsetUnits="MM" repeatDistance="0" distMapUnitScale="3x:0,0,0,0,0,0" dist="0" layerType="PolygonGeometry" offsetType="0" centroidWhole="0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGenerator="" maxCurvedCharAngleIn="25" repeatDistanceUnits="MM" priority="5" overrunDistance="0" overrunDistanceUnit="MM" geometryGeneratorEnabled="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" xOffset="0"/>
          <rendering displayAll="0" labelPerPart="0" scaleMin="0" obstacleType="0" scaleVisibility="0" fontMaxPixelSize="10000" upsidedownLabels="0" minFeatureSize="0" mergeLines="0" fontLimitPixelSize="0" fontMinPixelSize="3" maxNumLabels="2000" zIndex="0" obstacle="1" obstacleFactor="1" limitNumLabels="0" scaleMax="0" drawLabels="1"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
              <Option name="type" value="collection" type="QString"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option name="anchorPoint" value="pole_of_inaccessibility" type="QString"/>
              <Option name="ddProperties" type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
              <Option name="drawToAllParts" value="false" type="bool"/>
              <Option name="enabled" value="0" type="QString"/>
              <Option name="lineSymbol" value="&lt;symbol name=&quot;symbol&quot; alpha=&quot;1&quot; clip_to_extent=&quot;1&quot; type=&quot;line&quot; force_rhr=&quot;0&quot;>&lt;layer locked=&quot;0&quot; class=&quot;SimpleLine&quot; enabled=&quot;1&quot; pass=&quot;0&quot;>&lt;prop v=&quot;square&quot; k=&quot;capstyle&quot;/>&lt;prop v=&quot;5;2&quot; k=&quot;customdash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;customdash_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;customdash_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;draw_inside_polygon&quot;/>&lt;prop v=&quot;bevel&quot; k=&quot;joinstyle&quot;/>&lt;prop v=&quot;60,60,60,255&quot; k=&quot;line_color&quot;/>&lt;prop v=&quot;solid&quot; k=&quot;line_style&quot;/>&lt;prop v=&quot;0.3&quot; k=&quot;line_width&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;line_width_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;offset&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;offset_map_unit_scale&quot;/>&lt;prop v=&quot;MM&quot; k=&quot;offset_unit&quot;/>&lt;prop v=&quot;0&quot; k=&quot;ring_filter&quot;/>&lt;prop v=&quot;0&quot; k=&quot;use_custom_dash&quot;/>&lt;prop v=&quot;3x:0,0,0,0,0,0&quot; k=&quot;width_map_unit_scale&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString"/>
              <Option name="minLength" value="0" type="double"/>
              <Option name="minLengthMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="minLengthUnit" value="MM" type="QString"/>
              <Option name="offsetFromAnchor" value="0" type="double"/>
              <Option name="offsetFromAnchorMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offsetFromAnchorUnit" value="MM" type="QString"/>
              <Option name="offsetFromLabel" value="0" type="double"/>
              <Option name="offsetFromLabelMapUnitScale" value="3x:0,0,0,0,0,0" type="QString"/>
              <Option name="offsetFromLabelUnit" value="MM" type="QString"/>
            </Option>
          </callout>
        </settings>
      </rule>
    </rules>
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
    <DiagramCategory width="15" penColor="#000000" height="15" enabled="0" labelPlacementMethod="XHeight" penAlpha="255" scaleBasedVisibility="0" minScaleDenominator="0" minimumSize="0" opacity="1" rotationOffset="270" diagramOrientation="Up" lineSizeScale="3x:0,0,0,0,0,0" barWidth="5" penWidth="0" scaleDependency="Area" backgroundAlpha="255" sizeType="MM" maxScaleDenominator="1e+08" sizeScale="3x:0,0,0,0,0,0" lineSizeType="MM" backgroundColor="#ffffff">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute label="" field="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings showAll="1" dist="0" obstacle="0" zIndex="0" linePlacementFlags="18" priority="0" placement="1">
    <properties>
      <Option type="Map">
        <Option name="name" value="" type="QString"/>
        <Option name="properties"/>
        <Option name="type" value="collection" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration type="Map">
      <Option name="QgsGeometryGapCheck" type="Map">
        <Option name="allowedGapsBuffer" value="0" type="double"/>
        <Option name="allowedGapsEnabled" value="false" type="bool"/>
        <Option name="allowedGapsLayer" value="" type="QString"/>
      </Option>
    </checkConfiguration>
  </geometryOptions>
  <fieldConfiguration>
    <field name="Name">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="descriptio">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="timestamp">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="begin">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="end">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="altitudeMo">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="tessellate">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="extrude">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="visibility">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="drawOrder">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="icon">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Datetime">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" index="0" field="Name"/>
    <alias name="" index="1" field="descriptio"/>
    <alias name="" index="2" field="timestamp"/>
    <alias name="" index="3" field="begin"/>
    <alias name="" index="4" field="end"/>
    <alias name="" index="5" field="altitudeMo"/>
    <alias name="" index="6" field="tessellate"/>
    <alias name="" index="7" field="extrude"/>
    <alias name="" index="8" field="visibility"/>
    <alias name="" index="9" field="drawOrder"/>
    <alias name="" index="10" field="icon"/>
    <alias name="" index="11" field="Datetime"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" expression="" field="Name"/>
    <default applyOnUpdate="0" expression="" field="descriptio"/>
    <default applyOnUpdate="0" expression="" field="timestamp"/>
    <default applyOnUpdate="0" expression="" field="begin"/>
    <default applyOnUpdate="0" expression="" field="end"/>
    <default applyOnUpdate="0" expression="" field="altitudeMo"/>
    <default applyOnUpdate="0" expression="" field="tessellate"/>
    <default applyOnUpdate="0" expression="" field="extrude"/>
    <default applyOnUpdate="0" expression="" field="visibility"/>
    <default applyOnUpdate="0" expression="" field="drawOrder"/>
    <default applyOnUpdate="0" expression="" field="icon"/>
    <default applyOnUpdate="0" expression="" field="Datetime"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" constraints="0" field="Name" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" constraints="0" field="descriptio" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" constraints="0" field="timestamp" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" constraints="0" field="begin" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" constraints="0" field="end" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" constraints="0" field="altitudeMo" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" constraints="0" field="tessellate" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" constraints="0" field="extrude" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" constraints="0" field="visibility" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" constraints="0" field="drawOrder" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" constraints="0" field="icon" notnull_strength="0" unique_strength="0"/>
    <constraint exp_strength="0" constraints="0" field="Datetime" notnull_strength="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="Name" exp="" desc=""/>
    <constraint field="descriptio" exp="" desc=""/>
    <constraint field="timestamp" exp="" desc=""/>
    <constraint field="begin" exp="" desc=""/>
    <constraint field="end" exp="" desc=""/>
    <constraint field="altitudeMo" exp="" desc=""/>
    <constraint field="tessellate" exp="" desc=""/>
    <constraint field="extrude" exp="" desc=""/>
    <constraint field="visibility" exp="" desc=""/>
    <constraint field="drawOrder" exp="" desc=""/>
    <constraint field="icon" exp="" desc=""/>
    <constraint field="Datetime" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column hidden="1" type="actions" width="-1"/>
      <column name="Datetime" hidden="0" type="field" width="252"/>
      <column name="Name" hidden="0" type="field" width="-1"/>
      <column name="descriptio" hidden="0" type="field" width="351"/>
      <column name="timestamp" hidden="0" type="field" width="-1"/>
      <column name="begin" hidden="0" type="field" width="-1"/>
      <column name="end" hidden="0" type="field" width="-1"/>
      <column name="altitudeMo" hidden="0" type="field" width="-1"/>
      <column name="tessellate" hidden="0" type="field" width="-1"/>
      <column name="extrude" hidden="0" type="field" width="-1"/>
      <column name="visibility" hidden="0" type="field" width="-1"/>
      <column name="drawOrder" hidden="0" type="field" width="-1"/>
      <column name="icon" hidden="0" type="field" width="-1"/>
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
    <field editable="1" name="Datetime"/>
    <field editable="1" name="Name"/>
    <field editable="1" name="altitudeMo"/>
    <field editable="1" name="altitudeMode"/>
    <field editable="1" name="begin"/>
    <field editable="1" name="descriptio"/>
    <field editable="1" name="description"/>
    <field editable="1" name="drawOrder"/>
    <field editable="1" name="end"/>
    <field editable="1" name="extrude"/>
    <field editable="1" name="icon"/>
    <field editable="1" name="tessellate"/>
    <field editable="1" name="timestamp"/>
    <field editable="1" name="visibility"/>
  </editable>
  <labelOnTop>
    <field name="Datetime" labelOnTop="0"/>
    <field name="Name" labelOnTop="0"/>
    <field name="altitudeMo" labelOnTop="0"/>
    <field name="altitudeMode" labelOnTop="0"/>
    <field name="begin" labelOnTop="0"/>
    <field name="descriptio" labelOnTop="0"/>
    <field name="description" labelOnTop="0"/>
    <field name="drawOrder" labelOnTop="0"/>
    <field name="end" labelOnTop="0"/>
    <field name="extrude" labelOnTop="0"/>
    <field name="icon" labelOnTop="0"/>
    <field name="tessellate" labelOnTop="0"/>
    <field name="timestamp" labelOnTop="0"/>
    <field name="visibility" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>Name</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
