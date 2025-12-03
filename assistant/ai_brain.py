"""
AI Brain - Uses FREE Groq API with Llama models
"""

from groq import Groq
import config
import json

class AIBrain:
    def __init__(self, memory=None):
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.conversation_history = []
        self.memory = memory
        self.system_prompt = """You are JARVIS, a helpful AI assistant with access to the user's code editor and memory.
You can perform file operations, write code, and help with programming tasks.
You work within the Jarvis_Work folder in the user's Documents directory.

When the user asks you to work with files or code, use the available tools to:
- Read files
- Create new files and folders
- Modify existing files
- List directory contents
- Write or generate code

All paths are relative to the Jarvis_Work folder. Examples:
- "app.py" - file in root of workspace
- "myproject/main.py" - file in a subfolder
- "python_projects/game/game.py" - nested folders

Be concise but friendly in your responses. Keep answers under 2-3 sentences when possible.
"""
    
    def process_command(self, command, code_handler):
        """Process user command and return response"""
        
        # Add context from memory if available
        context = ""
        if self.memory:
            context = self.memory.get_context_summary()
        
        # Add user message to history with context
        user_message = command
        if context and len(self.conversation_history) == 0:  # First message
            user_message = f"{context}\n\nUser: {command}"
        
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Determine if this is a code-related task
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read the contents of a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to the file to read"
                            }
                        },
                        "required": ["file_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Write content to a file (creates new or overwrites existing)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to the file to write"
                            },
                            "content": {
                                "type": "string",
                                "description": "Content to write to the file"
                            }
                        },
                        "required": ["file_path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_files",
                    "description": "List files in a directory",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "directory": {
                                "type": "string",
                                "description": "Directory path (default: current directory)"
                            }
                        }
                    }
                }
            }
        ]
        
        # Call Groq (FREE) with function calling
        messages = [{"role": "system", "content": self.system_prompt}] + self.conversation_history
        
        response = self.client.chat.completions.create(
            model=config.GROQ_MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        
        # Handle function calls
        if tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Execute the function
                if function_name == "read_file":
                    result = code_handler.read_file(function_args["file_path"])
                elif function_name == "write_file":
                    result = code_handler.write_file(
                        function_args["file_path"],
                        function_args["content"]
                    )
                elif function_name == "list_files":
                    directory = function_args.get("directory", ".")
                    result = code_handler.list_files(directory)
                
                # Add function result to conversation
                self.conversation_history.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [tool_call.model_dump()]
                })
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })
            
            # Get final response after function execution
            messages = [{"role": "system", "content": self.system_prompt}] + self.conversation_history
            final_response = self.client.chat.completions.create(
                model=config.GROQ_MODEL,
                messages=messages
            )
            assistant_message = final_response.choices[0].message.content
        else:
            assistant_message = response_message.content
        
        # Add assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
