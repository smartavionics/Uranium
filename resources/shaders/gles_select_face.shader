[shaders]
vertex =
    #version 320 es
    uniform highp mat4 u_modelMatrix;
    uniform highp mat4 u_viewMatrix;
    uniform highp mat4 u_projectionMatrix;

    in highp vec4 a_vertex;

    void main()
    {
        gl_Position = u_projectionMatrix * u_viewMatrix * u_modelMatrix * a_vertex;
    }

geometry =
    #version 320 es

    layout(triangles) in;
    layout(triangle_strip, max_vertices = 3) out;

    void main()
    {
        gl_PrimitiveID = gl_PrimitiveIDIn;
        gl_Position = gl_in[0].gl_Position;
        EmitVertex();
        gl_Position = gl_in[1].gl_Position;
        EmitVertex();
        gl_Position = gl_in[2].gl_Position;
        EmitVertex();
    }

fragment =
    #version 320 es
    out highp vec4 frag_color;

    void main()
    {
        frag_color = vec4(0.0, 0.0, 0.0, 1.0);
        frag_color.r = float(gl_PrimitiveID % 0x100) / 255.0;
        frag_color.g = float((gl_PrimitiveID / 0x100) % 0x100) / 255.0;
        frag_color.b = float(0x1 + 2 * ((gl_PrimitiveID / 0x10000) % 0x80)) / 255.0;
        // Don't use alpha for anything, as some faces may be behind others, an only the front one's value is desired.
        // There isn't any control over the background color, so a signal-bit is put into the blue byte.
    }

[defaults]

[bindings]
u_modelMatrix = model_matrix
u_viewMatrix = view_matrix
u_projectionMatrix = projection_matrix

[attributes]
a_vertex = vertex
