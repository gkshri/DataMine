import java.io.*;
import org.json.*;
import org.json.simple.parser.*;
import java.lang.instrument.Instrumentation;
import java.time.*;
import java.util.Scanner;
import java.lang.AutoCloseable;

class dataminefinal implements AutoCloseable{

    static Instrumentation instrument;
    public static String FilePath;
    public 
    synchronized int Create(String Key, JSONObject Value, int TimeToLive) throws Exception
    {    
         if (Key.length()>32){
            System.out.println("Key size is more than 32");
            return 0;
         }
         else if((instrument.getObjectSize((Object)Value)/1024)>16){
            System.out.println("JSON object is more than 16KB");
            return 0;
         }
        try (FileReader reader = new FileReader(FilePath)){
            JSONTokener tokener = new JSONTokener(reader);
            JSONObject temp = new JSONObject(tokener);
            if (temp.has(Key)){
                System.out.println("KEY already exists.");
                return 0;
            }
            JSONArray NEW = new JSONArray();
            NEW.put(Value); 
            NEW.put(TimeToLive);
            LocalTime time = LocalTime.now();
            int TimeStamp = time.toSecondOfDay();
            NEW.put(TimeStamp);
            temp.put(Key, NEW);
            try (FileWriter file = new FileWriter(FilePath,false))
            {
                file.write(temp.toString());
                file.close();
                return 1;

            } catch (IOException e) {
                System.out.println("Caught IO Exception");
                return 0;
            }

        } catch (FileNotFoundException e){
            System.out.println("File Not Found");
            return 0;
        }
    }
    synchronized int Create(String Key, JSONObject Value) throws Exception
    {
    	if (Key.length()>32){
            System.out.println("Key size is more than 32");
            return 0;
        }       
    	else if((instrument.getObjectSize((Object)Value)/1024)>16){
            System.out.println(" Value size exceeds maximum size ");
            return 0;
        }
        try (FileReader reader = new FileReader(FilePath)) {
            JSONTokener tokener = new JSONTokener(reader);
            JSONObject NEW = new JSONObject(tokener);
            if (NEW.has(Key)){
                System.out.println("KEY already exists.");
                return 0;
            }
            JSONArray tempArray = new JSONArray();
            tempArray.put(Value);
            tempArray.put(Integer.MAX_VALUE); 
            LocalTime time = LocalTime.now();
            int TimeStamp = time.toSecondOfDay();
            tempArray.put(TimeStamp);
            NEW.put(Key, tempArray);
            try (FileWriter file = new FileWriter(FilePath,false))
            {
                file.write(NEW.toString());
                file.close();
                return 1;
            } 
            catch (IOException e) {
                System.out.println("Caught IO Exception");
            }
        }
        return 0;
    }
    synchronized JSONObject Read(String Key) throws Exception
    {
        try (FileReader reader = new FileReader(FilePath)) {
            JSONTokener tokener = new JSONTokener(reader);
            JSONObject temp = new JSONObject(tokener);
            if (temp.has(Key))
            {
                JSONArray NEW = new JSONArray();
                NEW = temp.getJSONArray(Key);
                LocalTime time = LocalTime.now();
                int CurrentTime = time.toSecondOfDay();
                //ttl check
                if ((CurrentTime - NEW.getInt(2)) < NEW.getInt(1))
                    return NEW.getJSONObject(0);
                else{
                System.out.println("Dead Key");
                return null;
                }
            }
            else{
                System.out.println("Invalid Key");
                return null;
            }
        } 
        catch (FileNotFoundException e) {
            System.out.println("File Not Found");
        } 
        catch (IOException e) {
            System.out.println("Caught IO Exception");
        }
		return null;
    }
    synchronized int Delete(String Key) throws Exception
    {
        try (FileReader reader = new FileReader(FilePath))
        {
        	JSONTokener tokener = new JSONTokener(reader);
            JSONObject temp = new JSONObject(tokener);
            if (temp.has(Key))
            {
                JSONArray NEW = new JSONArray();
                NEW = temp.getJSONArray(Key);
                LocalTime time = LocalTime.now();
                int CurrentTime = time.toSecondOfDay();
                //ttl check
                if ((CurrentTime - NEW.getInt(2)) < NEW.getInt(1))
                    temp.remove(Key);
                else{
                    System.out.println("Dead Key");
                    return 0;
                }
                try (FileWriter file = new FileWriter(FilePath,false))
                {
                    file.write(temp.toString());
                    file.close();
                    return 1;
                }
            }
            else{
                System.out.println("Invalid Key");
                return 0;
            }
        }
        catch (IOException e) {
            System.out.println("IO Exception");
        }
    return 0;
    }

    //-------------------------------------------------------constructors
    dataminefinal (String path) throws JSONException {
        FilePath = path;
        JSONObject fill = new JSONObject();
        fill.put(" ", " ");
         try (FileWriter file = new FileWriter(FilePath,false))
        		{
        	      file.write(fill.toString());
        	      file.close();
        		}
         catch (IOException E)
         {
        	System.out.println("Unable to create file"); 
         }
     }
    dataminefinal ()throws Exception {
        FilePath = "D://example.JSON";
        JSONObject fill = new JSONObject();
        fill.put(" ", " ");
         try (FileWriter file = new FileWriter(FilePath,false))
        		{
        	      file.write(fill.toString());
        	      file.close();
        		}
         catch (IOException E)
         {
        	System.out.println("Unable to create file"); 
         }
    }
    public static void main(String []args) {
        System.out.println("----dataMine----");
        System.out.println("----Enter file path----\n Defaults to D://example.JSON \n");
        Scanner sc = new Scanner(System.in);
        if(sc.hasNextLine()){
            FilePath=sc.nextLine();
            try(datamine cart = new datamine(FilePath)){
                handler(cart);
            }
            catch(Exception e){
                System.out.println(e);
            }
        }
        else{
            try(datamine cart= new datamine()){
                handler(cart);
            }
            catch(Exception e){
                System.out.print(e);
            }
        }
        sc.close();
    }
    public static void handler(datamine cart) {
     ////////////operations   
    }
    @Override
    public void close() throws IOException {
    }
}
