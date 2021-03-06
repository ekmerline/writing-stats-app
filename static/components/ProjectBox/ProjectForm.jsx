const { TextField, Button, FormControl, InputLabel, Select, MenuItem, Box  } = MaterialUI;

const ProjectForm = ({onSubmit, project_name, project_description, project_type_id, projectTypes, onChange, buttonText}) => {

    return (
        <React.Fragment>
            <Box>
                <TextField 
                    required 
                    name="project_name"
                    label="Project Name" 
                    placeholder="Project Name"
                    value={project_name} 
                    onChange={e => onChange(e)}
                />
            </Box>
            <Box>
                <TextField
                    required
                    multiline
                    name="project_description"
                    label="Project Description"
                    rows={5}
                    placeholder="Project Description"
                    value={project_description}
                    onChange={e => onChange(e)}
                />
            </Box>
            <Box>
                <FormControl style={{minWidth: 200}}>
                    <InputLabel id="project-type-label">Project Type</InputLabel>
                    <Select
                    labelId="project-type-label"
                    value={project_type_id}
                    name="project_type_id"
                    onChange={e => onChange(e)}
                    >
                    {projectTypes.map((projectType, index) => 
                        <MenuItem 
                        key={index} 
                        value={projectType['project_type_id']}>
                            {projectType['project_type_name']}
                        </MenuItem>
                    )}
                    </Select>
                </FormControl>
            </Box>
            <Box>
                <Button 
                    variant="contained" 
                    color="primary"
                    onClick={onSubmit}>
                    {buttonText}
                </Button>
            </Box>
        </React.Fragment>
    )
}