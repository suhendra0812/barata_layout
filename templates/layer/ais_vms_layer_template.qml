<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyLocal="1" minScale="1e+08" styleCategories="AllStyleCategories" labelsEnabled="1" simplifyMaxScale="1" simplifyDrawingHints="1" readOnly="0" simplifyDrawingTol="1" maxScale="0" simplifyAlgorithm="0" version="3.8.3-Zanzibar" hasScaleBasedVisibilityFlag="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 symbollevels="0" type="RuleRenderer" enableorderby="0" forceraster="0">
    <rules key="{1683a190-adbf-40aa-81d6-5d2c7a263b39}">
      <rule symbol="0" filter="$id = @atlas_featureid" label="DTO" key="{9eb1e871-e0d3-4f15-b54c-1f9dcf166a57}"/>
      <rule filter="ELSE" label="ELSE" key="{db4f6359-9984-43c6-bf0f-299a74a32b35}"/>
    </rules>
    <symbols>
      <symbol alpha="1" force_rhr="0" name="0" clip_to_extent="1" type="fill">
        <layer class="SimpleLine" pass="0" enabled="1" locked="0">
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
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <labeling type="rule-based">
    <rules key="{57f39956-59e1-4122-811e-3019b8bab361}">
      <rule filter="$id" key="{f1ba4df4-ebe8-4f18-857f-2d7bbee1bd48}">
        <settings>
          <text-style fontCapitals="0" namedStyle="Regular" textOpacity="1" previewBkgrdColor="#ffffff" isExpression="1" useSubstitutions="0" fontUnderline="0" fontSize="20" fontWordSpacing="0" fontSizeUnit="Point" fontItalic="0" fieldName=" @layer_name || day(to_datetime(&quot;Datetime&quot;) + to_interval('7 hours'))" fontWeight="50" blendMode="0" textColor="0,0,0,255" fontLetterSpacing="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" multilineHeight="1" fontStrikeout="0" fontFamily="MS Shell Dlg 2">
            <text-buffer bufferColor="255,255,255,255" bufferJoinStyle="128" bufferDraw="0" bufferSize="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferSizeUnits="MM" bufferNoFill="1" bufferBlendMode="0" bufferOpacity="1"/>
            <background shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeFillColor="255,255,255,255" shapeOffsetUnit="MM" shapeBorderColor="128,128,128,255" shapeJoinStyle="64" shapeRadiiX="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeSizeUnit="MM" shapeType="0" shapeDraw="0" shapeBlendMode="0" shapeBorderWidth="0" shapeSizeX="0" shapeOffsetX="0" shapeOffsetY="0" shapeSizeType="0" shapeSizeY="0" shapeRotationType="0" shapeOpacity="1" shapeSVGFile="" shapeRadiiY="0" shapeRadiiUnit="MM" shapeRotation="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthUnit="MM"/>
            <shadow shadowOffsetUnit="MM" shadowOffsetGlobal="1" shadowRadiusAlphaOnly="0" shadowOpacity="0.7" shadowBlendMode="6" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusUnit="MM" shadowDraw="0" shadowUnder="0" shadowScale="100" shadowOffsetDist="1" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetAngle="135" shadowRadius="1.5" shadowColor="0,0,0,255"/>
            <substitutions/>
          </text-style>
          <text-format autoWrapLength="0" rightDirectionSymbol=">" decimals="3" addDirectionSymbol="0" reverseDirectionSymbol="0" leftDirectionSymbol="&lt;" plussign="0" placeDirectionSymbol="0" formatNumbers="0" wrapChar="" multilineAlign="0" useMaxLineLengthForAutoWrap="1"/>
          <placement dist="0" distMapUnitScale="3x:0,0,0,0,0,0" centroidInside="0" placement="0" maxCurvedCharAngleOut="-25" geometryGeneratorEnabled="0" repeatDistanceUnits="MM" placementFlags="10" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" preserveRotation="1" geometryGeneratorType="PointGeometry" offsetType="0" yOffset="0" offsetUnits="MM" distUnits="MM" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" repeatDistance="0" rotationAngle="0" priority="5" geometryGenerator="" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" fitInPolygonOnly="0" maxCurvedCharAngleIn="25" quadOffset="4" centroidWhole="0" xOffset="0"/>
          <rendering scaleMax="0" scaleMin="0" obstacleFactor="1" upsidedownLabels="0" obstacle="1" fontMinPixelSize="3" displayAll="0" drawLabels="1" scaleVisibility="0" maxNumLabels="2000" zIndex="0" fontLimitPixelSize="0" minFeatureSize="0" fontMaxPixelSize="10000" obstacleType="0" labelPerPart="0" limitNumLabels="0" mergeLines="0"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </dd_properties>
        </settings>
      </rule>
    </rules>
  </labeling>
  <customproperties>
    <property key="dualview/previewExpressions" value="Name"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory penColor="#000000" labelPlacementMethod="XHeight" minScaleDenominator="0" lineSizeType="MM" height="15" sizeScale="3x:0,0,0,0,0,0" penWidth="0" width="15" enabled="0" scaleDependency="Area" penAlpha="255" backgroundColor="#ffffff" lineSizeScale="3x:0,0,0,0,0,0" maxScaleDenominator="1e+08" scaleBasedVisibility="0" minimumSize="0" barWidth="5" opacity="1" rotationOffset="270" sizeType="MM" backgroundAlpha="255" diagramOrientation="Up">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute color="#000000" label="" field=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings priority="0" zIndex="0" dist="0" linePlacementFlags="18" obstacle="0" placement="1" showAll="1">
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
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="Datetime">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="" field="Datetime"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" applyOnUpdate="0" field="Datetime"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" constraints="0" field="Datetime"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="Datetime"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortExpression="" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column width="-1" hidden="1" type="actions"/>
      <column width="252" name="Datetime" hidden="0" type="field"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
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
    <field editable="1" name="altitudeMode"/>
    <field editable="1" name="begin"/>
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
    <field labelOnTop="0" name="Datetime"/>
    <field labelOnTop="0" name="Name"/>
    <field labelOnTop="0" name="altitudeMode"/>
    <field labelOnTop="0" name="begin"/>
    <field labelOnTop="0" name="description"/>
    <field labelOnTop="0" name="drawOrder"/>
    <field labelOnTop="0" name="end"/>
    <field labelOnTop="0" name="extrude"/>
    <field labelOnTop="0" name="icon"/>
    <field labelOnTop="0" name="tessellate"/>
    <field labelOnTop="0" name="timestamp"/>
    <field labelOnTop="0" name="visibility"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>Name</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
