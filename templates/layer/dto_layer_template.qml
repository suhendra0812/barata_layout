<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="0" readOnly="0" simplifyLocal="1" simplifyDrawingTol="1" maxScale="0" simplifyMaxScale="1" minScale="1e+08" simplifyAlgorithm="0" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" version="3.8.2-Zanzibar" simplifyDrawingHints="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 symbollevels="0" type="RuleRenderer" forceraster="0" enableorderby="0">
    <rules key="{1683a190-adbf-40aa-81d6-5d2c7a263b39}">
      <rule filter="$id = @atlas_featureid" symbol="0" key="{9eb1e871-e0d3-4f15-b54c-1f9dcf166a57}" label="DTO"/>
      <rule filter="ELSE" key="{db4f6359-9984-43c6-bf0f-299a74a32b35}" label="ELSE"/>
    </rules>
    <symbols>
      <symbol type="fill" force_rhr="0" clip_to_extent="1" alpha="1" name="0">
        <layer pass="0" enabled="1" locked="0" class="SimpleLine">
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
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <customproperties>
    <property key="dualview/previewExpressions">
      <value>Name</value>
    </property>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory sizeType="MM" lineSizeType="MM" penWidth="0" scaleDependency="Area" minimumSize="0" rotationOffset="270" sizeScale="3x:0,0,0,0,0,0" diagramOrientation="Up" enabled="0" height="15" penColor="#000000" barWidth="5" lineSizeScale="3x:0,0,0,0,0,0" backgroundColor="#ffffff" width="15" scaleBasedVisibility="0" minScaleDenominator="0" backgroundAlpha="255" opacity="1" maxScaleDenominator="1e+08" labelPlacementMethod="XHeight" penAlpha="255">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute field="" color="#000000" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings priority="0" linePlacementFlags="18" obstacle="0" zIndex="0" placement="1" dist="0" showAll="1">
    <properties>
      <Option type="Map">
        <Option type="QString" name="name" value=""/>
        <Option name="properties"/>
        <Option type="QString" name="type" value="collection"/>
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
    <alias field="Datetime" index="0" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="Datetime" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint notnull_strength="0" field="Datetime" unique_strength="0" exp_strength="0" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="Datetime" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column hidden="1" type="actions" width="-1"/>
      <column hidden="0" type="field" width="252" name="Datetime"/>
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
    <field name="Datetime" labelOnTop="0"/>
    <field name="Name" labelOnTop="0"/>
    <field name="altitudeMode" labelOnTop="0"/>
    <field name="begin" labelOnTop="0"/>
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
