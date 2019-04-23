
import java.sql.*;

public class mysql{
    
    //    驱动类名
        String driver="com.mysql.jdbc.Driver";
    //    URL格式,最后为数据库名
        String url="jdbc:mysql://db4free.net:3306/baoxianjihuashu?useUnicode=true&characterEncoding=UTF8";//baoxianjihuashu为数据库名称
        String user="sandorn";
        String password="eeM3sh4KPkp4sJ8A";
        Connection  coon=null;

    public void close(){
            try{
                this.coon.close();
            }catch(Exception e){
                e.printStackTrace();
            }
        }

        public void select(){
            String sql="Select  *  from `"+"v爱守护"+"` Where 性别='男' and 年龄=45";//查询usrInfo表中的信息
            
            try{
                Statement stmt=(Statement)this.coon.createStatement();
                ResultSet rs=(ResultSet)stmt.executeQuery(sql);//得到的是结果的集合
                System.out.println("--------------------------------");
                System.out.println("姓名"+"\t"+"年龄"+"\t"+"性别");
                System.out.println("--------------------------------");
                while(rs.next()){
                    String name=rs.getString("性别");
                    int age=rs.getInt("年龄");
                    Number gender=rs.getDouble("费率");
                    System.out.println(name+"\t"+age+"\t"+gender);
                }
                stmt.close();
            }catch(Exception e){
                e.printStackTrace();
            }
        }
    }
