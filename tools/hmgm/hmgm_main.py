
class HmgmBase:
    """Abstract base class defining the API for all HMGM implementations, which are based on task management platforms."""
    
    def main():
        (output_file) = sys.argv[1]
        try:
            if task_exists() == False:
                create_task()
                exit(1) 
            else:
                if task_completed():
                    close_task()
                    write_output_file(output_file) # For testing only
                    exit(0)
                else:
                    exit(1)        
        except Exception as e:
            exit(-1)

    def task_completed():
       
        return True