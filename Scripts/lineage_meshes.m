%% MATLAB Lineage Tracts
% Creating 3D meshes for point clouds corresponding to Prat's Lineages
clear 
clc

% Suppressing all warning
warning("off","all")
warning

%% Parameter Setting
% Alpha Parameter for alphaShape
alpha   = 375;
%alpha   = "auto";
% Jitter to create an artificially higher number of points really close by
jitter  = 325; 
%jitter  = 375; 
% How densely to jitter the points
density = 12;

% Number of smoothing iterations 
numIterations = 13;
%numIterations = 14;

% Taubin Smoothing
scaleFactor = [0.55, -0.59];
%extraSmooth = 10;
extraSmooth = 12;
sizeFactor  = 1;

%% Point Cloud Path
scriptDir = fileparts(mfilename("fullpath"));
repoRoot  = fullfile(scriptDir, "..");
volRoot   = fullfile(repoRoot, "Analysis_Outputs", "Volumes");

tractStructs = dir(fullfile(volRoot, "Lineage_Tracts", "*", "*", "*.pcd"));
%tractStructs = dir(fullfile(volRoot, "Sensory_Bundles", "*", "*.pcd"));

% Initialize an empty cell array to hold the full paths
filePaths = cell(size(tractStructs, 1), 1);

% Construct full paths to the files
for k = 1:length(tractStructs)
    filePaths{k} = fullfile(tractStructs(k).folder, tractStructs(k).name);
end

%% Looping over each folder
parfor (i = 1:length(filePaths), 4)
%for i = 1:length(filePaths)
    try
        % Status
        cloudPath = filePaths{i};
        fprintf("\nWorking on %s\n", cloudPath)
    
        % Parse the Name 
        alphaName = replace(cloudPath, ".pcd", ".stl");
        
        % Generate the Shape
        [shp, bf, P] = generateShapeFromCloud(cloudPath, ...
                                                  jitter, ...
                                                  density, ...
                                                  alpha);
    
        % Write as an STL
        stlwrite(triangulation(bf, P), alphaName);
    
        % Smothing the Mesh
        smoothVol = smoothSTLTaubin(alphaName, numIterations, ...
            scaleFactor, sizeFactor, extraSmooth);

    catch ME
        fprintf(2, "✗ [%s] %s: %s\n", cloudPath, ME.identifier, ME.message);

    end

end

%% Display Status
disp("हो गया दोस्तों!!!")