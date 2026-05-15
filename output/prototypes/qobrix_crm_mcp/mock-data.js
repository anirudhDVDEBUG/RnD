// Mock Qobrix CRM data aligned with RESO DD 2.0 field naming

export const contacts = [
  {
    ContactId: "cnt-001",
    FirstName: "Sarah",
    LastName: "Al-Rashid",
    Email: "sarah@example.com",
    Phone: "+971-50-123-4567",
    ContactType: "Buyer",
    PreferredLocation: "Dubai Marina",
    Budget: 1800000,
    Currency: "USD",
    CreatedAt: "2026-03-15T10:30:00Z"
  },
  {
    ContactId: "cnt-002",
    FirstName: "James",
    LastName: "Chen",
    Email: "james.chen@example.com",
    Phone: "+971-55-987-6543",
    ContactType: "Seller",
    PreferredLocation: "Downtown Dubai",
    Budget: 3500000,
    Currency: "USD",
    CreatedAt: "2026-04-02T14:20:00Z"
  },
  {
    ContactId: "cnt-003",
    FirstName: "Maria",
    LastName: "Gonzalez",
    Email: "maria.g@example.com",
    Phone: "+971-52-555-0101",
    ContactType: "Buyer",
    PreferredLocation: "Palm Jumeirah",
    Budget: 5000000,
    Currency: "USD",
    CreatedAt: "2026-04-18T09:00:00Z"
  }
];

export const properties = [
  {
    ListingId: "prop-101",
    PropertyType: "Apartment",
    ListPrice: 1500000,
    Currency: "USD",
    StandardStatus: "Active",
    BedroomsTotal: 2,
    BathroomsTotalInteger: 2,
    LivingArea: 1200,
    LivingAreaUnits: "sqft",
    City: "Dubai",
    SubdivisionName: "Dubai Marina",
    CountryRegion: "UAE",
    ListingDescription: "Stunning 2BR apartment with full marina view, modern finishes",
    ListAgentFullName: "John Mitchell",
    ListDate: "2026-04-01T00:00:00Z"
  },
  {
    ListingId: "prop-102",
    PropertyType: "Villa",
    ListPrice: 4200000,
    Currency: "USD",
    StandardStatus: "Active",
    BedroomsTotal: 5,
    BathroomsTotalInteger: 6,
    LivingArea: 5500,
    LivingAreaUnits: "sqft",
    City: "Dubai",
    SubdivisionName: "Palm Jumeirah",
    CountryRegion: "UAE",
    ListingDescription: "Luxury beachfront villa with private pool and garden",
    ListAgentFullName: "Aisha Patel",
    ListDate: "2026-03-20T00:00:00Z"
  },
  {
    ListingId: "prop-103",
    PropertyType: "Apartment",
    ListPrice: 850000,
    Currency: "USD",
    StandardStatus: "Pending",
    BedroomsTotal: 1,
    BathroomsTotalInteger: 1,
    LivingArea: 750,
    LivingAreaUnits: "sqft",
    City: "Dubai",
    SubdivisionName: "JLT",
    CountryRegion: "UAE",
    ListingDescription: "Cozy 1BR in Jumeirah Lake Towers with lake view",
    ListAgentFullName: "John Mitchell",
    ListDate: "2026-04-10T00:00:00Z"
  },
  {
    ListingId: "prop-104",
    PropertyType: "Penthouse",
    ListPrice: 8500000,
    Currency: "USD",
    StandardStatus: "Active",
    BedroomsTotal: 4,
    BathroomsTotalInteger: 5,
    LivingArea: 4800,
    LivingAreaUnits: "sqft",
    City: "Dubai",
    SubdivisionName: "Downtown Dubai",
    CountryRegion: "UAE",
    ListingDescription: "Ultra-luxury penthouse with Burj Khalifa views",
    ListAgentFullName: "Aisha Patel",
    ListDate: "2026-02-15T00:00:00Z"
  }
];

export const leads = [
  {
    LeadId: "lead-201",
    ContactId: "cnt-001",
    ContactName: "Sarah Al-Rashid",
    Source: "Website",
    Status: "Qualified",
    AssignedAgent: "John Mitchell",
    PropertyInterest: "prop-101",
    Notes: "Interested in 2BR Marina apartments, budget up to $1.8M",
    CreatedAt: "2026-04-05T11:00:00Z"
  },
  {
    LeadId: "lead-202",
    ContactId: "cnt-003",
    ContactName: "Maria Gonzalez",
    Source: "Referral",
    Status: "New",
    AssignedAgent: "Aisha Patel",
    PropertyInterest: "prop-102",
    Notes: "Referred by existing client, looking for Palm villas",
    CreatedAt: "2026-04-20T16:30:00Z"
  },
  {
    LeadId: "lead-203",
    ContactId: "cnt-002",
    ContactName: "James Chen",
    Source: "Property Portal",
    Status: "Contacted",
    AssignedAgent: "John Mitchell",
    PropertyInterest: null,
    Notes: "Wants to sell Downtown apartment, requesting valuation",
    CreatedAt: "2026-04-22T08:45:00Z"
  }
];

export const opportunities = [
  {
    OpportunityId: "opp-301",
    LeadId: "lead-201",
    ContactName: "Sarah Al-Rashid",
    PropertyId: "prop-101",
    Stage: "Negotiation",
    Value: 1450000,
    Currency: "USD",
    Probability: 70,
    ExpectedCloseDate: "2026-05-30",
    AssignedAgent: "John Mitchell"
  },
  {
    OpportunityId: "opp-302",
    LeadId: "lead-202",
    ContactName: "Maria Gonzalez",
    PropertyId: "prop-102",
    Stage: "Viewing Scheduled",
    Value: 4200000,
    Currency: "USD",
    Probability: 30,
    ExpectedCloseDate: "2026-07-15",
    AssignedAgent: "Aisha Patel"
  }
];

export const tasks = [
  {
    TaskId: "task-401",
    Title: "Follow up with Sarah on offer",
    AssignedTo: "John Mitchell",
    RelatedEntity: "lead-201",
    DueDate: "2026-05-16",
    Status: "Pending",
    Priority: "High"
  },
  {
    TaskId: "task-402",
    Title: "Schedule property viewing for Maria",
    AssignedTo: "Aisha Patel",
    RelatedEntity: "lead-202",
    DueDate: "2026-05-18",
    Status: "Pending",
    Priority: "Medium"
  },
  {
    TaskId: "task-403",
    Title: "Prepare valuation report for James",
    AssignedTo: "John Mitchell",
    RelatedEntity: "lead-203",
    DueDate: "2026-05-20",
    Status: "In Progress",
    Priority: "High"
  }
];

export const users = [
  {
    UserId: "usr-01",
    FullName: "John Mitchell",
    Email: "john.m@agency.com",
    Role: "Senior Agent",
    Team: "Residential Sales",
    ActiveListings: 12,
    ClosedDeals: 45
  },
  {
    UserId: "usr-02",
    FullName: "Aisha Patel",
    Email: "aisha.p@agency.com",
    Role: "Senior Agent",
    Team: "Luxury Division",
    ActiveListings: 8,
    ClosedDeals: 38
  }
];
