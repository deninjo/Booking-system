# Movie Ticket Booking System

![Movie Ticket Booking System](https://i.ibb.co/CbD1gPQ/1.png)

A comprehensive Movie Ticketing System built with Python and MySQL that manages movie shows, customer bookings, seat selection, and pricing. The system includes data warehouse capabilities for analytics and supports distributed database architecture through master-slave replication.

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation-setup)
  - [Database Setup](#-database-setup)
  - [Remote Database Access](#-remote-database-access)
  - [Python Environment Setup](#-python-environment-setup)
- [Running the System](#-running-the-system)
- [Power BI Integration](#-power-bi-integration)
  - [ODBC Configuration](#-odbc-configuration)
  - [Power BI Connection](#-power-bi-connection)
  - [Data Warehouse Analytics](#-data-warehouse-analytics)
- [Database Distribution](#-database-distribution)
  - [Master-Slave Replication Setup](#-master-slave-replication-setup)
  - [Monitoring Replication](#-monitoring-replication)
- [Screenshots](https://github.com/deninjo/Booking-system/blob/master/Screenshots/README.md)
- [Contributing](#-contributing)


## ✨ Features 

- **Movie Management**: Add, view, and manage movie details
- **Show Scheduling**: Configure movie showtimes and theaters
- **Seat Selection**: Interactive seat booking with real-time availability
- **Customer Management**: Handle customer registration and booking history
- **Pricing System**: Dynamic pricing based on seat categories
- **Data Warehouse**: Built-in analytics and reporting capabilities
- **Power BI Integration**: Advanced data visualization and insights
- **Distributed Architecture**: Master-slave replication for scalability
- **Real-time Analytics**: Live dashboard updates and reporting

## 📁 Project Structure 

```
Booking-system/
│
├── main.py                              # Entry point to run the system
├── db.py                               # Database connection configuration
├── records.py                          # Python classes for the system
├── MySQL Database/                     # Database scripts
│   ├── ticket_booking.sql             # Database schema
│   └── Data Warehouse/                # Data warehouse scripts
│       ├── data_warehouse.sql         # Data warehouse schema
│       ├── Movie Ticketing System DW.pbix  # Power BI file
│       └── Visuals.PNG                # Power BI dashboard screenshot
├── Screenshots/                        # System screenshots
└── README.md                          # This documentation
```

## 🔧 Prerequisites 

Before setting up the system, ensure you have:

- **MySQL Server 8.0+** installed and running
- **Python 3.8+** with pip package manager
- **MySQL Connector/Python** library
- **Power BI Desktop** (for analytics)
- **MySQL ODBC Driver** (for Power BI integration)
- **Windows/Linux** operating system with appropriate permissions

## 🚀 Installation & Setup 

### Database Setup 

1. **Install MySQL Server**
   ```bash
   # Download and install MySQL Server 8.0+ from official website
   # https://dev.mysql.com/downloads/mysql/
   ```

2. **Create the Database**
   ```sql
   -- Connect to MySQL as root user
   mysql -u root -p
   
   -- Create the database
   CREATE DATABASE ticket_booking;
   USE ticket_booking;
   
   -- Import the database schema
   SOURCE /path/to/MySQL Database/ticket_booking.sql;
   
   -- Import the data warehouse schema
   SOURCE /path/to/MySQL Database/Data Warehouse/data_warehouse.sql;

   -- Copy contents from MySQL Database/Booking_trigger.txt and paste into MySQL
   ```

3. **Verify Database Setup**
   ```sql
   -- Check if tables are created
   SHOW TABLES;

   -- Check if triggers are created
   SHOW TRIGGERS;

### Remote Database Access 

To enable remote connections for Power BI and replication:

1. **Create Remote User**
   ```sql
   -- Create user with remote access
   CREATE USER 'remote_user'@'%' IDENTIFIED BY 'secure_password';
   
   -- Grant necessary privileges
   GRANT SELECT ON ticket_booking.* TO 'remote_user'@'%';
   
   -- Apply changes
   FLUSH PRIVILEGES;
   ```

2. **Configure MySQL for Remote Connections**
   
   Navigate to MySQL configuration file:
   - **Windows**: `C:\ProgramData\MySQL\MySQL Server 8.0\my.ini`
   - **Linux**: `/etc/mysql/mysql.conf.d/mysqld.cnf`
   
   Add or modify:
   ```ini
   [mysqld]
   bind-address = 0.0.0.0
   port = 3306
   ```

3. **Restart MySQL Service**
   ```bash
   # Windows
   net stop mysql80
   net start mysql80
   
   # Linux
   sudo systemctl restart mysql
   ```

4. **Configure Firewall to open Port 3306**
   ```bash
   # Windows (Run as Administrator)
   netsh advfirewall firewall add rule name="MySQL" dir=in action=allow protocol=TCP localport=3306
   
   # Linux
   sudo ufw allow 3306/tcp
   ```

### Python Environment Setup 

1. **Clone or Download the Repository**
   ```bash
   git clone <repository-url>
   cd Booking-system
   ```

2. **Install Required Python Packages**
   ```bash
   pip install mysql-connector-python
   pip install pandas
   pip install datetime
   ```

3. **Configure Database Connection**
   
   Edit `db.py` with your database credentials:
   ```python
   # Database connection parameters
   def get_db_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="ticket_booking"
    )
   ```

## 🎬 Running the System 

1. **Start the Application**
   ```bash
   python main.py
   ```

2. **System Navigation**
   
   The system provides a menu-driven interface with options for:
   - **Customer Registration**: Register new customers
   - **Movie Management**: Add/view movies and shows
   - **Booking System**: Select movies, shows, and seats
   - **View Bookings**: Check existing reservations
   - **Reports**: Generate booking and revenue reports

3. **Sample Workflow**
   ```
   1. Register as a customer
   2. Browse available movies
   3. Select a movie and showtime
   4. Choose preferred seats
   5. Confirm booking and payment
   6. Receive booking confirmation
   ```

## 📊 Power BI Integration 

### ODBC Configuration

1. **Install MySQL ODBC Driver**
   
   Download from: https://dev.mysql.com/downloads/connector/odbc/

2. **Configure ODBC Data Source**
   ```
   1. Press Win + R, type: odbcad32.exe
   2. Go to System DSN tab
   3. Click "Add" → Select "MySQL ODBC 8.0 Unicode Driver"
   4. Fill in details:
      - Data Source Name: MovieBooking_ODBC
      - TCP/IP Server: your_server_ip
      - Port: 3306
      - User: remote_user
      - Password: your_password
      - Database: ticket_booking
   5. Test connection
   6. Click OK to save
   ```

### Power BI Connection 

1. **Connect to Database**
   ```
   1. Open Power BI Desktop
   2. Home → Get Data → ODBC
   3. Select "MovieBooking_ODBC" from dropdown
   4. Choose authentication method
   5. Enter credentials if prompted
   ```

2. **Load Data Tables**
   
   **Option A: GUI Method**
   ```
   1. Select tables to import:
      - movies (Dimension)
      - customers (Dimension)
      - bookings (Fact)
      - seats (Dimension)
      - shows (Dimension)
   2. Click "Load" or "Transform Data" for cleaning
   ```
   
   **Option B: Custom SQL Query**
   ```sql
   -- Example aggregated query
   SELECT 
       m.movie_name,
       COUNT(b.booking_id) as total_bookings,
       SUM(b.total_amount) as revenue,
       AVG(b.total_amount) as avg_booking_value
   FROM bookings b
   JOIN shows s ON b.show_id = s.show_id
   JOIN movies m ON s.movie_id = m.movie_id
   GROUP BY m.movie_name
   ORDER BY revenue DESC;
   ```

### Data Warehouse Analytics 

The included Power BI file (`Movie Ticketing System DW.pbix`) provides:

- **Revenue Dashboard**: Daily, weekly, monthly revenue trends
- **Movie Performance**: Top-performing movies and shows
- **Customer Analytics**: Booking patterns and customer segments
- **Seat Utilization**: Theater occupancy and popular seating areas
- **Operational Metrics**: Peak hours, seasonal trends

**Key Measures Created:**
```dax
Total Revenue = SUM(bookings[total_amount])
Booking Count = COUNT(bookings[booking_id])
Average Ticket Price = DIVIDE([Total Revenue], [Booking Count])
Occupancy Rate = DIVIDE([Booked Seats], [Total Seats])
```

## 🔄 Database Distribution 

### Master-Slave Replication Setup 

#### Master Server Configuration 

1. **Create Replication User**
   ```sql
   -- On master server
   CREATE USER 'replica_user'@'%' IDENTIFIED WITH mysql_native_password BY 'replica_password';
   GRANT REPLICATION SLAVE ON *.* TO 'replica_user'@'%';
   FLUSH PRIVILEGES;
   ```

2. **Configure Master Server**
   
   Edit MySQL configuration file and add:
   ```ini
   [mysqld]
   server-id = 1
   log-bin = mysql-bin
   binlog-do-db = ticket_booking
   ```

3. **Restart MySQL and Check Status**
   ```sql
   -- Restart MySQL service, then:
   SHOW MASTER STATUS;
   ```
   Note the `File` and `Position` values for slave configuration.

#### Slave Server Configuration 

1. **Configure Slave Server**
   
   Edit MySQL configuration file:
   ```ini
   [mysqld]
   server-id = 2
   relay-log = slave-relay-bin
   log-bin = mysql-bin
   read-only = ON
   replicate-do-db = ticket_booking
   ```

2. **Synchronize Database**
   ```bash
   # Import data (if not already in sync)
   # On master server - create database dump
   mysqldump -u root -p --master-data=2 ticket_booking > ticket_booking_master.sql
   
   # Transfer file to slave server and import
   mysql -u root -p < ticket_booking_master.sql
   ```

3. **Configure Replication on Slave**
   ```sql
   -- On slave server
   STOP REPLICA;
   
   CHANGE MASTER TO
     MASTER_HOST = 'master_server_ip',
     MASTER_USER = 'replica_user',
     MASTER_PASSWORD = 'replica_password',
     MASTER_LOG_FILE = 'mysql-bin.000001',  -- From SHOW MASTER STATUS
     MASTER_LOG_POS = 154;                   -- From SHOW MASTER STATUS
   
   START REPLICA;
   ```

### Monitoring Replication 

```sql
-- Check replication status on slave
SHOW REPLICA STATUS\G

-- Key indicators to monitor:
-- Replica_IO_Running: Yes
-- Replica_SQL_Running: Yes  
-- Seconds_Behind_Source: 0
-- Last_Error: (should be empty)
```




## 📸 Screenshots

View detailed screenshots of the system in action:
[Screenshots of the working system](https://github.com/deninjo/Booking-system/blob/master/Screenshots/README.md)  

## 🤝 Contributing 

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



## 🆘 Support

If you encounter any issues:

1. Check the database connection in `db.py`
2. Verify MySQL service is running
3. Ensure all required Python packages are installed
4. Check firewall settings for remote connections
5. Verify ODBC driver installation for Power BI

For additional help, please open an issue in the repository.

---

**Author**: deninjo  
**Version**: 2.0  
**Last Updated**: 2025

> 💡 **Tip**: Start with a local setup first, then gradually implement remote access and replication as needed for your deployment requirements.
