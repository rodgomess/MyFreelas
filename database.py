import supabase

class SupabaseClient:
    def __init__(self, supabase_url, supabase_key):
        self.SUPABASE_URL = supabase_url
        self.SUPABASE_KEY = supabase_key
        self.supabase = supabase.create_client(supabase_url, supabase_key)
        self.schema_table = "projects_info"

    def insert(self, data):
        response = self.supabase.table(self.schema_table).insert(data).execute()
        return response

    def read(self):
        response = self.supabase.table(self.schema_table).select("*").execute().data
        return response

    def update(self, data, id, value):
        response = self.supabase.table(self.schema_table).update(data).eq(id, value).execute()
        return response
    
    def upsert(self, data):
        response = self.supabase.table(self.schema_table).upsert(data).execute()
        return response
    
    def delete(self, id, value):
        response = self.supabase.table(self.schema_table).delete().eq(id, value).execute()
        return response
    
    def read_filtered_favorable(self):
        response = self.supabase.table(self.schema_table).select("*").eq("decision", "favoravel").execute().data
        return response
    
    def read_filtered_agent(self):
        response = self.supabase.table(self.schema_table).select("*").is_("decision", None).execute().data
        return response
    
    def read_filtered_accepted(self):
        response = self.supabase.table(self.schema_table).select("*").eq("user_decision", "ACCEPTED").execute().data
        return response