query EIReviewsPageGraphQueryRG(
  $onlyCurrentEmployees: Boolean
  $employerId: Int!
  $jobTitle: JobTitleIdent
  $location: LocationIdent
  $employmentStatuses: [EmploymentStatusEnum]
  $goc: GOCIdent
  $highlight: HighlightTerm
  $page: Int!
  $sort: ReviewsSortOrderEnum
  $applyDefaultCriteria: Boolean
  $worldwideFilter: Boolean
  $language: String
  $preferredTldId: Int
  $isRowProfileEnabled: Boolean
  $dynamicProfileId: Int
  $useRowProfileTldForRatings: Boolean
) {
  employerReviews: employerReviewsRG(
    employerReviewsInput: {
      onlyCurrentEmployees: $onlyCurrentEmployees
      employer: { id: $employerId }
      jobTitle: $jobTitle
      location: $location
      goc: $goc
      employmentStatuses: $employmentStatuses
      highlight: $highlight
      sort: $sort
      page: { num: $page, size: 1000 }
      applyDefaultCriteria: $applyDefaultCriteria
      worldwideFilter: $worldwideFilter
      language: $language
      preferredTldId: $preferredTldId
      isRowProfileEnabled: $isRowProfileEnabled
      dynamicProfileId: $dynamicProfileId
      useRowProfileTldForRatings: $useRowProfileTldForRatings
    }
  ) {
    filteredReviewsCountByLang {
      count
      isoLanguage
      __typename
    }
    employer {
      legalActionBadges {
        id
        headerText
        bodyText
        __typename
      }
      bestPlacesToWork(onlyCurrent: true) {
        bannerImageUrl
        id
        isCurrent
        timePeriod
        __typename
      }
      bestProfile {
        id
        __typename
      }
      ceo {
        id
        name
        __typename
      }
      employerManagedContent(
        parameters: [
          { employerId: $employerId, divisionProfileId: $dynamicProfileId }
        ]
      ) {
        isContentPaidForTld
        __typename
      }
      id
      largeLogoUrl: squareLogoUrl(size: LARGE)
      links {
        jobsUrl
        reviewsUrl
        faqUrl
        __typename
      }
      regularLogoUrl: squareLogoUrl(size: REGULAR)
      shortName
      squareLogoUrl
      website
      __typename
    }
    queryLocation {
      id
      type
      shortName
      longName
      __typename
    }
    queryJobTitle {
      id
      text
      __typename
    }
    currentPage
    numberOfPages
    lastReviewDateTime
    allReviewsCount
    ratedReviewsCount
    filteredReviewsCount
    ratings {
      overallRating
      reviewCount
      ceoRating
      recommendToFriendRating
      cultureAndValuesRating
      diversityAndInclusionRating
      careerOpportunitiesRating
      workLifeBalanceRating
      seniorManagementRating
      compensationAndBenefitsRating
      businessOutlookRating
      ceoRatingsCount
      ratedCeo {
        id
        name
        title
        regularPhoto: photoUrl(size: REGULAR)
        largePhoto: photoUrl(size: LARGE)
        currentBestCeoAward {
          displayName
          timePeriod
          __typename
        }
        __typename
      }
      __typename
    }
    reviews {
      isLegal
      reviewId
      reviewDateTime
      ratingOverall
      ratingCeo
      ratingBusinessOutlook
      ratingWorkLifeBalance
      ratingCultureAndValues
      ratingDiversityAndInclusion
      ratingSeniorLeadership
      ratingRecommendToFriend
      ratingCareerOpportunities
      ratingCompensationAndBenefits
      employer {
        id
        shortName
        regularLogoUrl: squareLogoUrl(size: REGULAR)
        largeLogoUrl: squareLogoUrl(size: LARGE)
        __typename
      }
      isCurrentJob
      lengthOfEmployment
      employmentStatus
      jobEndingYear
      jobTitle {
        id
        text
        __typename
      }
      location {
        id
        type
        name
        __typename
      }
      originalLanguageId
      pros
      prosOriginal
      cons
      consOriginal
      summary
      summaryOriginal
      advice
      adviceOriginal
      isLanguageMismatch
      countHelpful
      countNotHelpful
      employerResponses {
        id
        response
        userJobTitle
        responseDateTime(format: ISO)
        countHelpful
        countNotHelpful
        responseOriginal
        languageId
        originalLanguageId
        translationMethod
        __typename
      }
      featured
      isCovid19
      topLevelDomainId
      languageId
      translationMethod
      __typename
    }
    ratingCountDistribution {
      overall {
        _5
        _4
        _3
        _2
        _1
        __typename
      }
      cultureAndValues {
        _5
        _4
        _3
        _2
        _1
        __typename
      }
      careerOpportunities {
        _5
        _4
        _3
        _2
        _1
        __typename
      }
      workLifeBalance {
        _5
        _4
        _3
        _2
        _1
        __typename
      }
      seniorManagement {
        _5
        _4
        _3
        _2
        _1
        __typename
      }
      compensationAndBenefits {
        _5
        _4
        _3
        _2
        _1
        __typename
      }
      diversityAndInclusion {
        _5
        _4
        _3
        _2
        _1
        __typename
      }
      recommendToFriend {
        WONT_RECOMMEND
        RECOMMEND
        __typename
      }
      __typename
    }
    __typename
  }
  pageViewSummary {
    totalCount
    __typename
  }
  reviewLocationsV2(employer: { id: $employerId }) {
    locations {
      atlasType
      id
      name
      __typename
    }
    employerHQLocation {
      atlasType
      id
      name
      __typename
    }
    __typename
  }
}

