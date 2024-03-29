
import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Market Share"
        self.description = "GEOG 5223 - Market share class project"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # Input Point Features parameter
        in_features_point = arcpy.Parameter(
            displayName   = "Input point features", # text shown in the interface
            name          = "in_features_point",    # use in Python when this tool is called by others
            datatype      = "GPFeatureLayer",       # Existing feature layer, or specify
            parameterType = "Required",             # Required, or optional
            direction     = "Input")                # Input parameter
        in_features_point.filter.list = ["Point"]   # Only allow Point feature classes

        # Field name parameter
        name_field       = arcpy.Parameter(
            displayName          = "Name Field",
            name                 = "name_field",
            datatype             = "Field",
            parameterType        = "Required",
            direction            = "Input")
        name_field.parameterDependencies = [in_features_point.name]
        
        #input polygon features parameter
        in_features_polygon = arcpy.Parameter(
            displayName     = "Input polygon features",
            name            = "in_features_polygon",
            datatype        = "GPFeatureLayer",
            parameterType   = "Required",
            direction       = "Input")
        in_features_polygon.filter.list = ['Polygon']


        # Polygon Join field parameter
        in_join_field = arcpy.Parameter(
            displayName   = 'Polygon join field',
            name          = 'in_join_field',
            datatype      = 'Field',
            parameterType = 'Required',
            direction     = 'Input')
        in_join_field.filter.list = ['String']
        in_join_field.parameterDependencies = [in_features_polygon.name]

        # polygon area field parameter
        in_area_field = arcpy.Parameter(
            displayName   = 'Polygon old area field',
            name          = 'in_area_field',
            datatype      = 'Field',
            parameterType = 'Required',
            direction     = 'Input')
        in_area_field.parameterDependencies = [in_features_polygon.name]

        #Population table parameter
        in_population_table = arcpy.Parameter(
            displayName   = 'Population table',
            name          = 'in_population_table',
            datatype      = 'GPTableView',
            parameterType = 'Required',
            direction     = 'Input')

        #population table join field parameter
        in_table_join_field = arcpy.Parameter(
            displayName   = 'Table join field',
            name          = 'in_table_join_field',
            datatype      = 'Field',
            parameterType = 'Required',
            direction     = 'Input')
        in_table_join_field.parameterDependencies = [in_population_table.name]

        #population table population field parameter
        in_table_population_field = arcpy.Parameter(
            displayName   = 'Population field',
            name          = 'in_table_population_field',
            datatype      = 'Field',
            parameterType = 'Required',
            direction     = 'Input')
        in_table_population_field.parameterDependencies = [in_population_table.name]

        # output feature parameter
        out_features = arcpy.Parameter(
            displayName   = "Output",
            name          = 'out_features',
            datatype      = 'GPFeatureLayer',
            parameterType = 'Required',
            direction     = 'output')

        params = [in_features_point,name_field ,in_features_polygon,in_join_field,
                  in_area_field, in_population_table,in_table_join_field,
                  in_table_population_field,out_features]
        
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        in_features_point          = parameters[0].valueAsText
        name_field                 = parameters[1].valueAsText
        in_features_polygon        = parameters[2].valueAsText
        in_join_field              = parameters[3].valueAsText
        in_area_field              = parameters[4].valueAsText
        in_population_table        = parameters[5].valueAsText
        in_table_join_field        = parameters[6].valueAsText
        in_table_population_field  = parameters[7].valueAsText
        out_features               = parameters[8].valueAsText


        arcpy.AddMessage(f'''Here are the specified -
            + Parameter 1: {in_features_point}
            + Parameter 2: {name_field}
            + Parameter 3: {in_features_polygon}
            + Parameter 4: {in_join_field}
            + Parameter 5: {in_area_field}
            + Parameter 6: {in_population_table}
            + Parameter 7: {in_table_join_field}
            + Parameter 8: {in_table_population_field}
            + Parameter 9: {out_features}
            + Scratch GDB: {arcpy.env.scratchGDB}''')

        #set environment
        desc = arcpy.da.Describe(in_features_polygon)
        arcpy.env.extent = desc['extent']
        arcpy.env.overwriteOutput = True
        # Step 1 calculate thiessen polygons for point features to extent of input polygon feature
        out_thiessen = arcpy.env.scratchGDB+"\\thiessen" #intermediate
        out_fields = 'ALL'
        arcpy.CreateThiessenPolygons_analysis(in_features_point,out_thiessen, out_fields)

        #Step 2 intersect polygon features to thiessen features
        out_inter = arcpy.env.scratchGDB+"\\intersect" #intermediate
        arcpy.analysis.Intersect([[in_features_polygon],[out_thiessen]], out_inter)

        #step 3 Join population table with intersected features
        arcpy.JoinField_management(out_inter, in_join_field, in_population_table, in_table_join_field, [in_table_population_field])
        
        #step 4 proportional population
        newField = 'propPop'
        arcpy.management.AddField(out_inter,newField,'DOUBLE')
        expression = f'!{in_table_population_field}!*(!Shape_Area!/!{in_area_field}!)'
        arcpy.management.CalculateField(out_inter, newField, expression, 'PYTHON3')
        

        #Step 5 Dissolve joined layer using the name field
        arcpy.management.Dissolve(out_inter,out_features, name_field, [[newField,"SUM"]])

        #Step 6 Add new field of population percentages to output layer
            #first get total pop
        sc = arcpy.da.SearchCursor(out_features, [f'SUM_{newField}'])
        totPop = sum([row[0] for row in sc])
            #now compute percent of pop
        pct = "Population Pct"
        arcpy.management.CalculateField(out_features, pct, f'(!SUM_{newField}!/{totPop})* 100', 'PYTHON3')
        arcpy.management.DeleteField(out_features,f'SUM_{newField}')
        

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return


