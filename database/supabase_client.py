import supabase
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, date, timezone

class SupabaseClient:
    def __init__(self):
        load_dotenv()
        self.SUPABASE_URL = os.getenv("SUPABASE_URL")
        self.SUPABASE_KEY = os.getenv("SUPABASE_KEY")
        self.supabase = supabase.create_client(self.SUPABASE_URL, self.SUPABASE_KEY)
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
    
    def delete_by_date_range(self, start_date: date, end_date: date):
        """
        Deleta registros com inserted_at entre [start_date 00:00:00, end_date 23:59:59.999],
        usando limites UTC (end exclusivo).
        """
        start_iso = datetime.combine(start_date, datetime.min.time()).replace(tzinfo=timezone.utc).isoformat()
        end_iso   = (datetime.combine(end_date,   datetime.min.time()) + timedelta(days=1)).replace(tzinfo=timezone.utc).isoformat()

        return (
            self.supabase
            .table(self.schema_table)
            .delete()
            .gte("inserted_at", start_iso)
            .lt("inserted_at", end_iso)
            .execute()
        )
    
    def read_filtered_favorable(self):
        response = self.supabase.table(self.schema_table).select("*").eq("decision", "favoravel").execute().data
        return response
    
    def read_filtered_agent(self):
        response = self.supabase.table(self.schema_table).select("*").is_("decision", None).execute().data
        return response
    
    def read_filtered_accepted(self):
        response = self.supabase.table(self.schema_table).select("*").eq("user_decision", "ACCEPTED").execute().data
        return response
    
    def read_to_front(self):
        response = self.supabase.table(self.schema_table).select("*").neq("decision", None).execute().data
        return response